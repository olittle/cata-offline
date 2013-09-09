/*-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
*
* File Name : cast2Int.java
*
* Purpose : cast a sring in the file into int 
*
* Creation Date : 11-06-2013
*
* Last Modified : Tue 11 Jun 2013 02:13:05 PM PDT
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

public class cast2Int extends EvalFunc<Integer>{
    public Integer exec(Tuple input) throws IOException {
            if (input == null || input.size() == 0)
                      return 0;
                  try{
                              String str = (String)input.get(0);
                              return Integer.parseInt(str);
                  }
                        catch(Exception e){
                          throw WrappedIOException.wrap("Caught exception processing input row ", e);
                        }
    }
}
