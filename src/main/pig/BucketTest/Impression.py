#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Impression.py
#
# Purpose :
#
# Creation Date : 22-07-2013
#
# Last Modified : Wed 07 Aug 2013 09:48:51 AM PDT
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
        
%declare OUTPUT '/user/haliu'
member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();
imprs = LOAD '/data/tracking/ImpressionTrackingEvent' USING LiAvroStorage('date.range','start.date=$DATA_DATE;end.date=$DATA_DATE;error.on.missing=false');

-- filter sponsored jobs and JYMBII impression on homepage
imprs = FILTER imprs BY (impressionType == 'rj_hp_mimp');

impr = foreach imprs generate (int)header.memberId as memberId, 
                        (long)header.time as time, 
                        (int)contents#'job_id' as jobId;
impr = filter impr by memberId > 0 and jobId > 0; 

impr = join impr by memberId, member by memberId parallel 2000; 
impr = foreach impr generate impr::memberId as memberId, impr::time as time, impr::jobId as jobId;
impr = distinct impr parallel 1;
STORE impr INTO '$OUTPUT/JYMBII-batch/history/impression/$REPORT_DATE' USING BinaryJSON('memberId'); 

    """

    prog = Pig.compile(script) 
    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()



