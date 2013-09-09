#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : ViewPairs.py
#
# Purpose :
#
# Creation Date : 22-07-2013
#
# Last Modified : Wed 07 Aug 2013 09:48:39 AM PDT
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

#     ('date.range','start.date=$DATE;end.date=$DATE;error.on.missing=false');

    script = """
%declare OUTPUT '/user/haliu'
member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();
events = LOAD '/data/tracking/PageViewEvent' USING LiAvroStorage('date.range','start.date=$DATA_DATE;end.date=$DATA_DATE;error.on.missing=false');

job_view_events = FILTER events BY requestHeader.pageKey == 'jobs_seeking_view_job' AND header.memberId > 0;

job_views = FOREACH job_view_events GENERATE 
  (int)header.memberId   AS memberId,
  (long)header.time      AS time,
  trackingCode,
  (int)trackingInfo#'0'  AS jobId;

job_views = join job_views by memberId, member by memberId; 
job_views = foreach job_views generate job_views::memberId as memberId, job_views::time as time, job_views::jobId as jobId;
job_views = filter job_views by memberId > 0; 
 
job_views = distinct job_views parallel 1;
STORE job_views INTO '$OUTPUT/JYMBII-batch/history/view/$REPORT_DATE' USING BinaryJSON('memberId');

    """

    prog = Pig.compile(script) 
    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()
        print "********************************Finish Current Data " + para['DATE'] + " *************************************************"
