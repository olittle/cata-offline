---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Positive.pig
--
-- Purpose :
--
-- Creation Date : 26-07-2013
--
-- Last Modified : Wed 07 Aug 2013 02:06:50 PM PDT
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

RMF $OUTPUT/JYMBII-batch/history/positive/$REPORT_DATE
RMF $OUTPUT/JYMBII-batch/history/positive/$DELETE_DATE

applypair = LOAD '/data/tracking/JobApplyClickEvent' USING LiAvroStorage('date.range','start.date=$DATA_DATE;end.date=$DATA_DATE;error.on.missing=false');
applypair = foreach applypair generate header.memberId as memberId, jobId, header.time as time;

member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();

applypair = join applypair by memberId, member by memberId parallel 2000;
applypair = foreach applypair generate applypair::memberId as memberId, applypair::jobId as jobId, applypair::time as time; 

applypair = distinct applypair parallel 1;  
store applypair into '$OUTPUT/JYMBII-batch/history/positive/$REPORT_DATE' USING BinaryJSON('memberId'); 
