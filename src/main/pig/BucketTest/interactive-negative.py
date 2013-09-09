#!/usr/bin/python

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : interactive-negative.py
#
# Purpose :
#
# Creation Date : 23-07-2013
#
# Last Modified : Wed 07 Aug 2013 09:49:14 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from org.apache.pig.scripting import Pig
import os 

if __name__ == "__main__":

    params = [] 
    
    prefix = "2013070"
    for i in range(1, 10):
        day = prefix + str(i)
        par = {}
        par['DATA_DATE'] = day
        par['REPORT_DATE'] = "2013/07/0" + str(i) 
        params.append(par) 

    prefix = "201307"
    for i in range(10, 32):
        day = prefix + str(i)
        par = {}
        par['DATA_DATE'] = day
        par['REPORT_DATE'] = "2013/07/" + str(i) 
        params.append(par) 
    
    
    prefix = "2013080"
    for i in range(1, 10):
        day = prefix + str(i)
        par = {}
        par['DATA_DATE'] = day
        par['REPORT_DATE'] = "2013/08/0" + str(i) 
        params.append(par) 
    

    script = """
register './impr_no_click.py' using jython as myfuncs;
%declare OUTPUT '/user/haliu'
impr = LOAD '$OUTPUT/JYMBII-batch/history/impression/$REPORT_DATE' USING BinaryJSON();
view = LOAD '$OUTPUT/JYMBII-batch/history/view/$REPORT_DATE' USING BinaryJSON();
impr = foreach impr generate memberId, time, jobId;
view = foreach view generate memberId, time, jobId;

non_view = cogroup impr by memberId inner, view by memberId inner; 
non_view = foreach non_view generate group as memberId, myfuncs.NonView(impr, view) as negs; 

non_view = filter non_view by not IsEmpty(negs); 
non_view = foreach non_view generate memberId, FLATTEN(negs);
non_view = foreach non_view generate memberId, negs::jobId as jobId; 
non_view = distinct non_view parallel 1;
 
store non_view into '$OUTPUT/JYMBII-batch/history/impression-inter-neg/$REPORT_DATE' USING BinaryJSON('memberId'); 
    """

    prog = Pig.compile(script) 
    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()
