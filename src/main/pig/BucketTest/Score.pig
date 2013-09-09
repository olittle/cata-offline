---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Tuple.pig
--
-- Purpose : Generate Tuples for each members 
--
-- Creation Date : 24-07-2013
--
-- Last Modified : Thu 08 Aug 2013 09:10:15 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  5
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now + $tzoffset))`
%declare szero    `echo $(($now - 60 * 60 * 24 * $daysago + $tzoffset))`

%declare S_DATA_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$szero" "+%Y%m%d"; else date -r $szero "+%Y%m%d"; fi'`
%declare T_DATA_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y%m%d"; else date -r $tzero "+%Y%m%d"; fi'`
%declare x `echo $T_DATA_DATE`
%declare x `echo $S_DATA_DATE`

RMF $OUTPUT/JYMBII-batch/TMP/history

define AVG org.apache.pig.builtin.AVG();

data = load '$OUTPUT/JYMBII-batch/$DIR/history-data-collection' USING BinaryJSON();

-- data = foreach data generate memberId, jobId, class, RANDOM() as rand;
-- SPLIT data INTO training IF rand >= 0.05, testing IF rand < 0.05;
-- 
-- training = foreach training generate 't' as label, class, memberId, jobId; 
-- testing = foreach testing generate 'c' as label, class, memberId, jobId; 
-- 
-- data = union training, testing; 

-- score = load '$OUTPUT/JYMBII-batch/history/recent-score' USING BinaryJSON('date.range','start.date=$S_DATA_DATE;end.date=$T_DATA_DATE;error.on.missing=false');
-- score2 = load '$OUTPUT/JYMBII-batch/TMP/member_job_score_post' USING BinaryJSON();
-- score = union score, score2;

score = load '$OUTPUT/JYMBII-batch/TMP/member_job_score_post' USING BinaryJSON();

score = foreach score generate sourceId as memberId, FLATTEN(hits);
score = foreach score generate memberId, hits::id as jobId, hits::score as score;

score = group score by (memberId, jobId) parallel 1000;
score = foreach score generate group.memberId as memberId, group.jobId as jobId, AVG(score.score) as score; 

data = join score by (memberId, jobId), data by (memberId, jobId) using 'replicated';

data = distinct data parallel 5; 
-- data = foreach data generate data::label as label, data::class as class, data::memberId as memberId, data::jobId as jobId, score::score as score;   
data = foreach data generate data::class as class, data::memberId as memberId, data::jobId as jobId, score::score as score;   

STORE data into '$OUTPUT/JYMBII-batch/TMP/history' USING BinaryJSON('memberId');

data = load '$OUTPUT/JYMBII-batch/TMP/test-collection' USING BinaryJSON();

data = join score by (memberId, jobId), data by (memberId, jobId) using 'replicated';

data = distinct data parallel 5;
 
data = foreach data generate data::class as class, data::memberId as memberId, data::jobId as jobId, score::score as score;   
data = foreach data generate 'p' as label, class, memberId, jobId, score; 
STORE data into '$OUTPUT/JYMBII-batch/TMP/test' USING BinaryJSON('memberId');

