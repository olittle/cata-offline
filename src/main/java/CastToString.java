/*-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
*
* File Name : CastToString.java
*
* Purpose : Cast a int to String 
*
* Creation Date : 11-06-2013
*
* Last Modified : Tue 11 Jun 2013 03:08:54 PM PDT
*
* Created By : Huan Gui (hgui@linkedin.com) 
*
*_._._._._._._._._._._._._._._._._._._._._.*/


package com.linkedin.liar.pigUDFs;

import java.io.*;
import java.lang.Integer;
import java.lang.String;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;
import org.apache.pig.impl.util.WrappedIOException;
import org.apache.pig.data.DataType;

public class CastToString extends EvalFunc<String>{
    public String exec(Tuple input) throws IOException {
            if (input == null || input.size() == 0)
                      return null;
                  try{
                              Integer CompanyId = (Integer) input.get(0);
                              return CompanyId.toString();
                  }
                        catch(Exception e){
                          throw WrappedIOException.wrap("Caught exception processing input row ", e);
                        }
    }
}
