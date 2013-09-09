---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Delete.pig
--
-- Purpose :
--
-- Creation Date : 19-07-2013
--
-- Last Modified : Thu 08 Aug 2013 06:49:52 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default start    `echo $(($now/(60*60*24)*60*24*60))` 
%declare n `echo $now`
%declare s `echo $start` 
%default daysago  30
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($start - 60 * 60 * 24 * $daysago + $tzoffset))`
%declare nzero    `echo $(($now - 60 * 60 * 24 + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$nzero" "+%Y/%m/%d"; else date -r $nzero "+%Y/%m/%d"; fi'`
%declare e `echo $REPORT_DATE`
%declare s1  `echo $tzero` 

RMF $OUTPUT/JYMBII-batch/history/delete/$REPORT_DATE

neg1 = LOAD '/data/databases/DPDB/ENTITY_FEEDBACK/#LATEST' USING LiAvroStorage();

neg1 = foreach neg1 generate SOURCE_ENTITY_ID as memberId, (int)TARGET_ENTITY_ID as jobId:int, LAST_MODIFIED as time;
neg1 = filter neg1 by time > $tzero; 

member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();

data = join neg1 by memberId, member by memberId parallel 2000;
data = foreach data generate neg1::memberId as memberId, neg1::jobId as jobId, neg1::time as time;

-- member = load '$OUTPUT/JYMBII-batch/TMP/MemList' USING BinaryJSON();
-- data = join data by memberId, member by memberId;
-- data = foreach data generate data::memberId as memberId, data::jobId as jobId, data::time as time; 
data = distinct data parallel 1; 

STORE data INTO '$OUTPUT/JYMBII-batch/history/delete/$REPORT_DATE' USING BinaryJSON('memberId'); 
