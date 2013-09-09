#!/usr/bin/python

#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Positive.py
#
# Purpose : Generate Pig script for each day 
#
# Creation Date : 22-07-2013
#
# Last Modified : Wed 07 Aug 2013 09:49:23 AM PDT
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
    
    
    Pig.registerUDF("attribute_click.py", "myfuncs")

    script = """
%declare OUTPUT '/user/haliu'
        applypair = LOAD '/data/tracking/JobApplyClickEvent' USING LiAvroStorage('date.range','start.date=$DATA_DATE;end.date=$DATA_DATE;error.on.missing=false');
        applypair = foreach applypair generate header.memberId as memberId, jobId, header.time as time;
        
        member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();
        
        applypair = join applypair by memberId, member by memberId parallel 2000;
        applypair = foreach applypair generate applypair::memberId as memberId, applypair::jobId as jobId, applypair::time as time; 
        
        applypair = distinct applypair parallel 1;  
        store applypair into '$OUTPUT/JYMBII-batch/history/positive/$REPORT_DATE' USING BinaryJSON('memberId'); 
    """

    prog = Pig.compile(script) 
    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()
