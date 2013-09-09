---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : RecentScore.pig
--
-- Purpose : Get the recent score that cannot be calculated by CROWN ( the job is too new)
--
-- Creation Date : 03-08-2013
--
-- Last Modified : Fri 09 Aug 2013 02:50:54 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com)
--
--_._._._._._._._._._._._._._._._._._._._._.


%declare kernel   `uname -s`
%default now      `date "+%s"`
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now + $tzoffset))`
%declare TODAY `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y/%m/%d"; else date -r $tzero "+%Y/%m/%d"; fi'`
%declare x `echo $TODAY`


%declare dzero    `echo $(($now - 60 * 60 * 24 * 5 +$tzoffset))`
%declare DELETE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$dzero" "+%Y/%m/%d"; else date -r $dzero "+%Y/%m/%d"; fi'`
%declare x `echo $DELETE`

RMF $OUTPUT/JYMBII-batch/history/recent-score/$DELETE
RMF $OUTPUT/JYMBII-batch/history/recent-score/$TODAY

--member = load '$OUTPUT/JYMBII-batch/MemberList' USING BinaryJSON();
data = load '/data/derived/liar/jymbii/jymbii-batch/recs/#LATEST' USING BinaryJSON();
--data = join data by sourceId, member by memberId PARALLEL 2000;
--data = foreach data generate 18041 as algorithmId, data::computeTime as computeTime, data::hits as hits, data::intent as intent, data::lastMod as lastMod, data::returnStatus as returnStatus, data::sourceId as sourceId;
data = filter data by sourceId == 18041;
--data = distinct data parallel 10;

store data into '$OUTPUT/JYMBII-batch/history/recent-score/$TODAY' USING BinaryJSON('intent', 'algorithmId', 'sourceId');
