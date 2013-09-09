---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : ViewPairs.pig
--
-- Purpose :
--
-- Creation Date : 26-07-2013
--
-- Last Modified : Thu 08 Aug 2013 06:55:30 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  1
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now - 60 * 60 * 24 * $daysago + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y/%m/%d"; else date -r $tzero "+%Y/%m/%d"; fi'`
%declare DATA_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y%m%d"; else date -r $tzero "+%Y%m%d"; fi'`
%declare e `echo $REPORT_DATE`
%declare x `echo $DATA_DATE`

%declare dzero    `echo $(($now - 60 * 60 * 24 * 40 + $tzoffset))`
%declare DELETE_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$dzero" "+%Y%m%d"; else date -r $dzero "+%Y%m%d"; fi'`
%declare y `echo $DELETE_DATE`

RMF $OUTPUT/JYMBII-batch/TMP
RMF $OUTPUT/JYMBII-batch/history/view/$REPORT_DATE
RMF $OUTPUT/JYMBII-batch/history/view/$DELETE_DATE

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

