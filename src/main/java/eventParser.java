/*-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
 *
 * File Name : parser.java
 *
 * Purpose : parse the content of user feature file
 *
 * Creation Date : 11-06-2013
 *
 * Last Modified : Tue 11 Jun 2013 02:31:09 PM PDT
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

public class eventParser extends EvalFunc<Integer> {
	public Integer exec(Tuple input) throws IOException {
		if (input == null || input.size() == 0)
			return -1;
		// list of all events 
		String [] Events = {"f_conn_invt_send", "f_conn_invt_receive", "f_conn_invt_accept",	// Connection Activity  
				"f_abook_impt", 							// address book importation activity 
				"f_sch", 	                                                        // search activity
				"f_job_app#click", "f_job_app#db", 					// job application activity 
				"f_inmail_send", "f_inmail_receive", "f_inmail_accept", 		// email activity 
				"f_subs_start", "f_subs_cancel", 					// premium subscription and cancel activity
				"f_pv#all", 							// all kinds of profile viewving activity 
				"f_adv", "f_adc", "f_adn"						// ads click, view, and 
		};
		// event_size = 16
		int event_size = Events.length;

		try{
			String Record = (String)input.get(0);
			int position = 0;								// record if specific activity is found
			int EventType = -1;
			for(int i = 0; i < event_size; i ++)
			{
				position = Record.indexOf(Events[i]);
				if(position != -1)
					EventType = i;
				break;
			}
			if(position == -1) 
				return null; 
			return EventType; 
		}
	
	catch(Exception e){
		throw WrappedIOException.wrap("Caught exception processing input row ", e);
	}
    }

}

