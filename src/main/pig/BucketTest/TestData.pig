---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : TestData.pig
--
-- Purpose : Generate the Test Data 
--
-- Creation Date : 28-07-2013
--
-- Last Modified : Fri 09 Aug 2013 01:34:42 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  4
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`

-- We only need to change the input data and test data
-- the dates range of training data are [$TODAY - 30, $TODAY - 5]
-- the dates range of testing data are [$TODAY - 4, $TODAY - 1]

 
%declare tzero    `echo $(($now - 60 * 60 * 24  + $tzoffset))`
%declare szero    `echo $(($now - 60 * 60 * 24 * $daysago + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y%m%d"; else date -r $tzero "+%Y%m%d"; fi'`
%declare START_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$szero" "+%Y%m%d"; else date -r $szero "+%Y%m%d"; fi'`
%declare e `echo $REPORT_DATE`
%declare x `echo $START_DATE`

RMF $OUTPUT/JYMBII-batch/TMP/test-collection

register 'set_minus.py' using jython as set_minus;

-- Positive Data: Users who click the apply button 
pos = LOAD '$INPUT/JYMBII-batch/history/positive' USING BinaryJSON('date.range', 'start.date=$START_DATE;end.date=$REPORT_DATE;error.on.missing=false');
pos = foreach pos generate memberId, jobId; 

--  Negative Data: Users who delete the recommendation 
-- because each snapshot of delete data contains previous 30 day worth of data, hence we need only 1 snapshot
del = LOAD '$INPUT/JYMBII-batch/history/delete' USING BinaryJSON('date.range', 'start.date=$REPORT_DATE;end.date=$REPORT_DATE;error.on.missing=false');
del = foreach del generate memberId, jobId; 

--  Negative Data: Viewed but did not apply 
view = LOAD '$INPUT/JYMBII-batch/history/view' USING BinaryJSON('date.range', 'start.date=$START_DATE;end.date=$REPORT_DATE;error.on.missing=false');
view = foreach view generate memberId, jobId;

--  Negative Data: Interactive Negative 
impr = load '$INPUT/JYMBII-batch/history/impression-inter-neg/' USING BinaryJSON('date.range', 'start.date=$START_DATE;end.date=$REPORT_DATE;error.on.missing=false');
impr = foreach impr generate memberId, jobId;

-- impr = join impr by memberId, member by memberId; 
-- impr = foreach impr generate impr::memberId as memberId, impr::jobId as jobId; 
 
data = cogroup pos by memberId, del by memberId, view by memberId, impr by memberId PARALLEL 1000;
data = foreach data generate group as memberId, pos.jobId as pos_jobs, del.jobId as del_jobs, view.jobId as view_jobs, impr.jobId as impr_jobs; 

-- view_jobs - pos_jobs - del_jobs
view_data = foreach data generate memberId, set_minus.Constraints2(view_jobs, pos_jobs, del_jobs) as jobIds; 
view_data = foreach view_data generate memberId, FLATTEN(jobIds), 1 as class;
view_data = foreach view_data generate memberId, jobIds::jobId as jobId, class; 

-- impr_jobs - pos_jobs - view_jobs - del_jobs
impr_data = foreach data generate memberId, set_minus.Constraints3(impr_jobs, pos_jobs, del_jobs, view_jobs) as jobIds; 
impr_data = foreach impr_data generate memberId, FLATTEN(jobIds), 2 as class; 
impr_data = foreach impr_data generate memberId, jobIds::jobId as jobId, class; 


pos = foreach pos generate memberId, jobId, 0 as class;
del = foreach del generate memberId, jobId, 3 as class;
data = union pos, del, view_data, impr_data;
data = distinct data parallel 2;

store data into '$OUTPUT/JYMBII-batch/TMP/test-collection' USING BinaryJSON('memberId');
