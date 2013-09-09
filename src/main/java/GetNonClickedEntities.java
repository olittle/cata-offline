package com.linkedin.liar.pigUDFs;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.TreeMap;

import org.apache.pig.EvalFunc;
import org.apache.pig.backend.hadoop.executionengine.mapReduceLayer.PigHadoopLogger;
import org.apache.pig.data.BagFactory;
import org.apache.pig.data.DataBag;
import org.apache.pig.data.DataType;
import org.apache.pig.data.Tuple;
import org.apache.pig.data.TupleFactory;
import org.apache.pig.impl.logicalLayer.FrontendException;
import org.apache.pig.impl.logicalLayer.schema.Schema;
import org.apache.pig.impl.util.UDFContext;

/**
 * "path" : { "string" : "3603" }
 * 
 * "path" : { "string" : "first-equity-partners" }
 * 
 * "path" : { "string" : "http://www.linkedin.com/company/860999" }
 * 
 * * "path" : { "string" : "http://www.linkedin.com/company/the-black-hole" }
 * 
 * @author haliu
 * 
 */

public class GetNonClickedEntities extends EvalFunc<DataBag>
{

  public enum TypeCounters
  {
    NUMERAL_PATHS,
    ALPHA_PATHS,
    URL_WITH_TRAILING_NUMERAL_PATHS,
    URL_WITH_TRAILING_ALPHA_PATHS;
  }

  public enum WarnCounters
  {
    NULL_INPUT, NULL_MATCH_COMP_ID;
  }

  private static final String IMP_BAG_ALIASES_PROPERTY = "impBagAliases";
  private static final String CLK_BAG_ALIASES_PROPERTY = "clkBagAliases";

  @Override
  public DataBag exec(Tuple input) throws IOException
  {
    // if (input == null || input.size() == 0)
    // {
    // pigLogger.warn(this, "input is null", WarnCounters.NULL_INPUT);
    // return null;
    // }

    if (input.size() != 2)
      throw new IllegalArgumentException("requires two parameters");

    if (!(input.get(0) instanceof DataBag) || !(input.get(1) instanceof DataBag))
      throw new IllegalArgumentException("expects a bag");

    DataBag res = BagFactory.getInstance().newDefaultBag();
    if (this.pigLogger == null)
      this.setPigLogger(PigHadoopLogger.getInstance());

    // retrieve the map from alias to field position

    Map<String, Map<String, Integer>> aliases = getFieldAliases();
    Map<String, Integer> impAliasPosMap = aliases.get(IMP_BAG_ALIASES_PROPERTY);
    Map<String, Integer> clkAliasPosMap = aliases.get(CLK_BAG_ALIASES_PROPERTY);

    // process impBag first
    DataBag impBag = (DataBag) input.get(0);
    // time --> a set of company ids (sorted by time)
    Map<Long, Set<Object>> impressionsGroupedByTime = new TreeMap<Long, Set<Object>>();
    Iterator<Tuple> it = impBag.iterator();
    while (it.hasNext())
    {
      Tuple tuple = it.next();
      Long time = (Long) tuple.get(impAliasPosMap.get("time"));
      Set<Object> impressedCompanies = new HashSet<Object>();
      DataBag impInnerBag = (DataBag) tuple.get(impAliasPosMap.get("companyIds"));
      Iterator<Tuple> innerIt = impInnerBag.iterator();
      while (innerIt.hasNext())
      {
        Object companyId = innerIt.next().get(0);
        impressedCompanies.add(companyId);
      }
      impressionsGroupedByTime.put(time, impressedCompanies);
    }

    System.out.println("impressions:");
    for (Long time : impressionsGroupedByTime.keySet())
    {
      System.out.print(time + ":\t");
      System.out.println(Arrays.toString(impressionsGroupedByTime.get(time).toArray()));
    }

    // then process the clkBag
    DataBag clkBag = (DataBag) input.get(1);
    // time --> companyId
    // supposing one can't click more than one impressions at the exact same time
    Map<Long, Object> clicksGroupedByTime = new HashMap<Long, Object>();
    it = clkBag.iterator();
    while (it.hasNext())
    {
      Tuple tuple = it.next();
      Long time = (Long) tuple.get(clkAliasPosMap.get("time"));
      // System.out.println(clkAliasPosMap.get("companyId"));
      Object company = tuple.get(clkAliasPosMap.get("companyId"));
      clicksGroupedByTime.put(time, company);
    }

    System.out.println("clicks:");
    for (Long time : clicksGroupedByTime.keySet())
    {
      System.out.println(time + ":\t" + clicksGroupedByTime.get(time));
    }

    // now attribute clicks to impressions
    Map<Long, Set<Object>> clicksGroupedByImpressionTime =
        new HashMap<Long, Set<Object>>();
    List<Long> listOfImpressionTimes = new ArrayList<Long>();
    listOfImpressionTimes.addAll(impressionsGroupedByTime.keySet());
    for (Long clickTime : clicksGroupedByTime.keySet())
    {
      Object clickedCompany = clicksGroupedByTime.get(clickTime);
      Long attributedImpressionTime;
      // the position returned should most likely be (-(insertion point) - 1), because
      // it's most likely that the click time is not contained in the impression times
      int index = Collections.binarySearch(listOfImpressionTimes, clickTime);
      if (index >= 0) // unlikely
        attributedImpressionTime = listOfImpressionTimes.get(index);
      else if (index == -1)
        attributedImpressionTime = null; // meaning no such impression time exists. This
                                         // could be due to the cut-off in data collection
      else
        attributedImpressionTime = listOfImpressionTimes.get(-index - 2);

      if (attributedImpressionTime != null)
      {
        if (clicksGroupedByImpressionTime.containsKey(attributedImpressionTime))
        {
          clicksGroupedByImpressionTime.get(attributedImpressionTime).add(clickedCompany);
        }
        else
        {
          Set<Object> clicksAttributedToThisTime = new HashSet<Object>();
          clicksAttributedToThisTime.add(clickedCompany);
          clicksGroupedByImpressionTime.put(attributedImpressionTime,
                                            clicksAttributedToThisTime);
        }
      }
    }

    System.out.println("attributed clicks:");
    for (Long time : clicksGroupedByImpressionTime.keySet())
    {
      System.out.print(time + ":\t");
      System.out.println(Arrays.toString(clicksGroupedByImpressionTime.get(time)
                                                                      .toArray()));
    }

    // now the difference between attributed clicks and impressions are the negative
    // examples for a given impression of 9 cymwtf companies. We want the union of all
    // such examples.
    Set<Object> negatives = new HashSet<Object>();
    Set<Object> positives = new HashSet<Object>();
    for (Long time : clicksGroupedByImpressionTime.keySet())
    {
      Set<Object> clickedCompanies = clicksGroupedByImpressionTime.get(time);
      Set<Object> impressedCompanies = impressionsGroupedByTime.get(time);
      Set<Object> diff = new HashSet<Object>(impressedCompanies);
      diff.removeAll(clickedCompanies);
      System.out.println(Arrays.toString(impressedCompanies.toArray()));
      System.out.println(Arrays.toString(clickedCompanies.toArray()));
      System.out.println(Arrays.toString(diff.toArray()));
      negatives.addAll(diff);
      positives.addAll(clickedCompanies);
    }
    negatives.removeAll(positives);
    System.out.println("negatives:");
    System.out.println(Arrays.toString(negatives.toArray()));

    // constructing the output from the set of negatives
    for (Object negativeCompanies : negatives)
    {
      Tuple t = TupleFactory.getInstance().newTuple(negativeCompanies);
      res.add(t);
    }
    return res;
  }

  public Schema outputSchema(Schema input)
  {
    if (input.size() != 2)
      throw new IllegalArgumentException("requires two parameters");
    try
    {

      if (input.getField(0).type != DataType.BAG
          || input.getField(1).type != DataType.BAG)
      {
        String msg =
            "Expected input (Bag_of impressions, Bag_of_clicks), received schema (";
        msg += DataType.findTypeName(input.getField(0).type);
        msg += ", ";
        msg += DataType.findTypeName(input.getField(1).type);
        msg += ")";
        throw new IllegalArgumentException(msg);
      }

      Schema impTupleSchema = input.getField(0).schema.getField(0).schema;
      Schema clkTupleSchema = input.getField(1).schema.getField(0).schema;

      Set<String> impBagAliases = impTupleSchema.getAliases();
      Set<String> clkBagAliases = clkTupleSchema.getAliases();

      if (!impBagAliases.contains("companyIds") || !impBagAliases.contains("time")
          || !clkBagAliases.contains("companyId") || !clkBagAliases.contains("time"))
      {
        String msg = "Expected both input bags to contain aliases 'companyId' and 'time'";
        throw new IllegalArgumentException(msg);
      }

      Schema impInnerBagSchema = impTupleSchema.getField("companyIds").schema;
      if (impInnerBagSchema.size() != 1
          || impInnerBagSchema.getField(0).type != DataType.TUPLE)
        throw new IllegalArgumentException("The inner bag 'companyIds' of $0 must contain only one field of the type tuple.");

      // store the schema fields, so we can reference them by string instead of position
      // in exec()
      storeInputFields(impTupleSchema, clkTupleSchema);
    }
    catch (FrontendException e)
    {
      e.printStackTrace();
    }

    Schema.FieldSchema companyId =
        new Schema.FieldSchema("companyId", DataType.CHARARRAY);
    Schema.FieldSchema companyIdTuple = new Schema.FieldSchema("null", DataType.TUPLE);
    companyIdTuple.schema = new Schema();
    companyIdTuple.schema.add(companyId);
    // user should name the bag
    Schema.FieldSchema companyIds = new Schema.FieldSchema(null, DataType.BAG);
    companyIds.schema = new Schema();
    companyIds.schema.add(companyIdTuple);
    return new Schema(companyIds);
  }

  /**
   * Retrieve the mapping from alias to field position from the Context
   */
  @SuppressWarnings("unchecked")
  private Map<String, Map<String, Integer>> getFieldAliases()
  {
    UDFContext context = UDFContext.getUDFContext();
    Properties properties = context.getUDFProperties(this.getClass());
    Map<String, Integer> impTupleAliases =
        (HashMap<String, Integer>) properties.get(IMP_BAG_ALIASES_PROPERTY);
    Map<String, Integer> clkTupleAliases =
        (HashMap<String, Integer>) properties.get(CLK_BAG_ALIASES_PROPERTY);
    if (impTupleAliases == null || clkTupleAliases == null)
    {
      log.error("Properties: " + properties);
      throw new RuntimeException("Could not retrieve aliases from properties using "
          + "fieldAliases");
    }
    Map<String, Map<String, Integer>> res = new HashMap<String, Map<String, Integer>>();
    res.put(IMP_BAG_ALIASES_PROPERTY, impTupleAliases);
    res.put(CLK_BAG_ALIASES_PROPERTY, clkTupleAliases);
    return res;
  }

  /**
   * Save the field aliases order, so we can look up easily in the exec() function
   * 
   * @param impTupleSchema
   */
  private void storeInputFields(Schema impTupleSchema, Schema clkTupleSchema)
  {
    Map<String, Integer> impTupleAliases = new HashMap<String, Integer>();
    Map<String, Integer> clkTupleAliases = new HashMap<String, Integer>();

    try
    {
      impTupleAliases.put("companyIds", impTupleSchema.getPosition("companyIds"));
      impTupleAliases.put("time", impTupleSchema.getPosition("time"));
      clkTupleAliases.put("companyId", clkTupleSchema.getPosition("companyId"));
      clkTupleAliases.put("time", clkTupleSchema.getPosition("time"));
    }
    catch (FrontendException e)
    {
      e.printStackTrace();
    }

    for (Map.Entry<String, Integer> en : impTupleAliases.entrySet())
    {
      System.out.print("impression bag: (" + en.getKey() + ", " + en.getValue() + ") ");
    }
    System.out.println();
    for (Map.Entry<String, Integer> en : clkTupleAliases.entrySet())
    {
      System.out.print("click bag: (" + en.getKey() + ", " + en.getValue() + ") ");
    }
    System.out.println();

    // pass the input schema into the exec function
    UDFContext context = UDFContext.getUDFContext();
    Properties properties = context.getUDFProperties(this.getClass());
    properties.put(IMP_BAG_ALIASES_PROPERTY, impTupleAliases);
    properties.put(CLK_BAG_ALIASES_PROPERTY, clkTupleAliases);
  }

  public static void main(String[] args) throws IOException
  {
    Schema.FieldSchema companyId =
        new Schema.FieldSchema("companyId", DataType.CHARARRAY);
    Schema.FieldSchema companyIdTuple = new Schema.FieldSchema("null", DataType.TUPLE);
    companyIdTuple.schema = new Schema();
    companyIdTuple.schema.add(companyId);
    Schema.FieldSchema companyIds = new Schema.FieldSchema("companyIds", DataType.BAG);
    companyIds.schema = new Schema();
    companyIds.schema.add(companyIdTuple);
    Schema.FieldSchema time = new Schema.FieldSchema("time", DataType.LONG);
    Schema.FieldSchema impBag = new Schema.FieldSchema("imprs", DataType.BAG);
    Schema.FieldSchema impTuple = new Schema.FieldSchema("null", DataType.TUPLE);
    impTuple.schema = new Schema();
    impTuple.schema.add(time);
    impTuple.schema.add(companyIds);
    impBag.schema = new Schema();
    impBag.schema.add(impTuple);

    Schema.FieldSchema clkBag = new Schema.FieldSchema("clicks", DataType.BAG);
    Schema.FieldSchema clkTuple = new Schema.FieldSchema("null", DataType.TUPLE);
    clkTuple.schema = new Schema();
    clkTuple.schema.add(time);
    clkTuple.schema.add(companyId);
    clkBag.schema = new Schema();
    clkBag.schema.add(clkTuple);

    Schema schema = new Schema();
    schema.add(impBag);
    schema.add(clkBag);

    GetNonClickedEntities udf = new GetNonClickedEntities();
    udf.outputSchema(schema);

    DataBag imp = BagFactory.getInstance().newDefaultBag();
    for (int i = 0; i < 5; i++)
    {
      Tuple t = TupleFactory.getInstance().newTuple(2);
      t.set(0, (long) (100000000000L * Math.random()));
      DataBag ids = BagFactory.getInstance().newDefaultBag();
      for (int j = 0; j < 10; j++)
      {
        Tuple tt = TupleFactory.getInstance().newTuple(1);
        tt.set(0, j);
        ids.add(tt);
      }
      t.set(1, ids);
      imp.add(t);
    }

    DataBag clk = BagFactory.getInstance().newDefaultBag();
    for (int i = 0; i < 3; i++)
    {
      Tuple t = TupleFactory.getInstance().newTuple(2);
      t.set(0, (long) (100000000000L * Math.random()));
      t.set(1, (int) (10 * Math.random()));
      clk.add(t);
    }

    Tuple input = TupleFactory.getInstance().newTuple(2);
    input.set(0, imp);
    input.set(1, clk);
    udf.exec(input);
    //
    // Tuple t2 =
    // TupleFactory.getInstance().newTuple("http://www.linkedin.com/company/860999");
    // Tuple t3 = TupleFactory.getInstance().newTuple("3603");
    // Tuple t4 =
    // TupleFactory.getInstance().newTuple("http://www.linkedin.com/www.prestat.nl");
    //
    // PageViewPathToLong pvp2l = new PageViewPathToLong();
    // try
    // {
    // System.out.println(pvp2l.exec(t1));
    // System.out.println(pvp2l.exec(t2));
    // System.out.println(pvp2l.exec(t3));
    // System.out.println(pvp2l.exec(t4));
    // }
    // catch (IOException e)
    // {
    // // TODO Auto-generated catch block
    // e.printStackTrace();
    // }
  }
}
