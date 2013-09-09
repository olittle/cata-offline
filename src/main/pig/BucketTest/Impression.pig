---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Impression.pig
--
-- Purpose :
--
-- Creation Date : 26-07-2013
--
-- Last Modified : Thu 08 Aug 2013 06:49:01 AM PDT
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


RMF $OUTPUT/JYMBII-batch/history/impression/$REPORT_DATE
RMF $OUTPUT/JYMBII-batch/history/impression/$DELETE_DATE

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
