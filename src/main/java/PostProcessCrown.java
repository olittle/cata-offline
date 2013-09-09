package com.linkedin.jymbii_crown;

import java.io.IOException;
import java.util.Map;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reporter;

import azkaban.common.utils.Props;

import com.linkedin.batch.serialization.AbstractJsonHadoopJob;
import com.linkedin.batch.serialization.JsonMapper;

public class PostProcessCrown extends AbstractJsonHadoopJob
{
  public PostProcessCrown(String id, Props props)
  {
    super(id, props);
  }

  @Override
  public void run() throws Exception
  {
    Props props = super.getProps();
    JobConf conf = createJobConf(PostProcessCrownResultsMapper.class);
    conf.setNumReduceTasks(props.getInt("num.reduce.tasks"));

    if (props.getBoolean("force.output.overwrite", false))
    {
      Path outputPath = new Path(props.getString("output.path"));
      FileSystem fileSystem = outputPath.getFileSystem(conf);
      fileSystem.delete(outputPath);
    }

    JobClient.runJob(conf);
  }

  public static class PostProcessCrownResultsMapper extends JsonMapper {

    @Override
    public void mapObjects(Object key,
                           Object value,
                           OutputCollector<Object, Object> output,
                           Reporter reporter) throws IOException
    {
      Map valueData = (Map) value;
      Map keyData = (Map) key;

      valueData.put("sourceId", keyData.get("sourceId"));
      valueData.put("intent", keyData.get("intent"));
      valueData.remove("numHits");
      output.collect(keyData, valueData);
    }
  }
}
