/*
 *  * To get the substring of a tuple
 *   */
package com.linkedin.liar.pigUDFs;

import java.io.*;
import java.lang.Integer;
import java.lang.String;
import org.apache.pig.EvalFunc;
import org.apache.pig.data.Tuple;
import org.apache.pig.impl.util.WrappedIOException;

public class substring extends EvalFunc<Integer>{
    public Integer exec(Tuple input) throws IOException {
            if (input == null || input.size() == 0)
                      return 0;
                  try{
                              String str = (String)input.get(0);
                              String member = str.split(":")[1];
                              return Integer.parseInt(member);
                  }
                        catch(Exception e){
                          throw WrappedIOException.wrap("Caught exception processing input row ", e);
                        }
    }
}

