---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Data-Collect.pig
--
-- Purpose : Collect data for each learning instance 
--
-- Creation Date : 31-07-2013
--
-- Last Modified : Fri 09 Aug 2013 02:21:13 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

-- $INDEX  index of which learning instance being processed


%declare X `pig Data-Collect-prep.pig`
%declare LS `ls -l /tmp/python*`
%declare ELS `echo $LS`

register logit.py using jython as myudfs; 
RMF $OUTPUT/JYMBII-batch/TMP/final-score-tmp

%declare kernel   `uname -s`
%default now      `date "+%s"`
%default daysago  1
%declare tzoffset `bash -c 'if [[ "$kernel" == "Linux" ]]; then echo "-28800";  else echo "0"; fi'`
%declare tzero    `echo $(($now + $tzoffset))`

%declare REPORT_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y/%m/%d"; else date -r $tzero "+%Y/%m/%d"; fi'`
%declare DATA_DATE `bash -c 'if [[ "$kernel" == "Linux" ]]; then date -d "@$tzero" "+%Y%m%d"; else date -r $tzero "+%Y%m%d"; fi'`
%declare e `echo $REPORT_DATE`
%declare x `echo $DATA_DATE`


-- Get the score of hit, i.e., for the subset - i, the features of both member and job are calculated 

%declare target0 `bash ./cmd.bash 0`
hit0 = load '$OUTPUT/JYMBII-batch/output/python-out-0/_files/Ztest$target0/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_0 `echo 0`
%declare echo2_0 `echo $target0`

%declare target1 `bash ./cmd.bash 1`
hit1 = load '$OUTPUT/JYMBII-batch/output/python-out-1/_files/Ztest$target1/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_1 `echo 1`
%declare echo2_1 `echo $target1`

%declare target2 `bash ./cmd.bash 2`
hit2 = load '$OUTPUT/JYMBII-batch/output/python-out-2/_files/Ztest$target2/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_2 `echo 2`
%declare echo2_2 `echo $target2`

%declare target3 `bash ./cmd.bash 3`
hit3 = load '$OUTPUT/JYMBII-batch/output/python-out-3/_files/Ztest$target3/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_3 `echo 3`
%declare echo2_3 `echo $target3`

%declare target4 `bash ./cmd.bash 4`
hit4 = load '$OUTPUT/JYMBII-batch/output/python-out-4/_files/Ztest$target4/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_4 `echo 4`
%declare echo2_4 `echo $target4`

%declare target5 `bash ./cmd.bash 5`
hit5 = load '$OUTPUT/JYMBII-batch/output/python-out-5/_files/Ztest$target5/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_5 `echo 5`
%declare echo2_5 `echo $target5`

%declare target6 `bash ./cmd.bash 6`
hit6 = load '$OUTPUT/JYMBII-batch/output/python-out-6/_files/Ztest$target6/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_6 `echo 6`
%declare echo2_6 `echo $target6`

%declare target7 `bash ./cmd.bash 7`
hit7 = load '$OUTPUT/JYMBII-batch/output/python-out-7/_files/Ztest$target7/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_7 `echo 7`
%declare echo2_7 `echo $target7`

%declare target8 `bash ./cmd.bash 8`
hit8 = load '$OUTPUT/JYMBII-batch/output/python-out-8/_files/Ztest$target8/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_8 `echo 8`
%declare echo2_8 `echo $target8`

%declare target9 `bash ./cmd.bash 9`
hit9 = load '$OUTPUT/JYMBII-batch/output/python-out-9/_files/Ztest$target9/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_9 `echo 9`
%declare echo2_9 `echo $target9`

%declare target10 `bash ./cmd.bash 10`
hit10 = load '$OUTPUT/JYMBII-batch/output/python-out-10/_files/Ztest$target10/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_10 `echo 10`
%declare echo2_10 `echo $target10`

%declare target11 `bash ./cmd.bash 11`
hit11 = load '$OUTPUT/JYMBII-batch/output/python-out-11/_files/Ztest$target11/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_11 `echo 11`
%declare echo2_11 `echo $target11`

%declare target12 `bash ./cmd.bash 12`
hit12 = load '$OUTPUT/JYMBII-batch/output/python-out-12/_files/Ztest$target12/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_12 `echo 12`
%declare echo2_12 `echo $target12`

%declare target13 `bash ./cmd.bash 13`
hit13 = load '$OUTPUT/JYMBII-batch/output/python-out-13/_files/Ztest$target13/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_13 `echo 13`
%declare echo2_13 `echo $target13`

%declare target14 `bash ./cmd.bash 14`
hit14 = load '$OUTPUT/JYMBII-batch/output/python-out-14/_files/Ztest$target14/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_14 `echo 14`
%declare echo2_14 `echo $target14`

%declare target15 `bash ./cmd.bash 15`
hit15 = load '$OUTPUT/JYMBII-batch/output/python-out-15/_files/Ztest$target15/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_15 `echo 15`
%declare echo2_15 `echo $target15`

%declare target16 `bash ./cmd.bash 16`
hit16 = load '$OUTPUT/JYMBII-batch/output/python-out-16/_files/Ztest$target16/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_16 `echo 16`
%declare echo2_16 `echo $target16`

%declare target17 `bash ./cmd.bash 17`
hit17 = load '$OUTPUT/JYMBII-batch/output/python-out-17/_files/Ztest$target17/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_17 `echo 17`
%declare echo2_17 `echo $target17`

%declare target18 `bash ./cmd.bash 18`
hit18 = load '$OUTPUT/JYMBII-batch/output/python-out-18/_files/Ztest$target18/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_18 `echo 18`
%declare echo2_18 `echo $target18`

%declare target19 `bash ./cmd.bash 19`
hit19 = load '$OUTPUT/JYMBII-batch/output/python-out-19/_files/Ztest$target19/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_19 `echo 19`
%declare echo2_19 `echo $target19`

%declare target20 `bash ./cmd.bash 20`
hit20 = load '$OUTPUT/JYMBII-batch/output/python-out-20/_files/Ztest$target20/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_20 `echo 20`
%declare echo2_20 `echo $target20`

%declare target21 `bash ./cmd.bash 21`
hit21 = load '$OUTPUT/JYMBII-batch/output/python-out-21/_files/Ztest$target21/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_21 `echo 21`
%declare echo2_21 `echo $target21`

%declare target22 `bash ./cmd.bash 22`
hit22 = load '$OUTPUT/JYMBII-batch/output/python-out-22/_files/Ztest$target22/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_22 `echo 22`
%declare echo2_22 `echo $target22`

%declare target23 `bash ./cmd.bash 23`
hit23 = load '$OUTPUT/JYMBII-batch/output/python-out-23/_files/Ztest$target23/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_23 `echo 23`
%declare echo2_23 `echo $target23`

%declare target24 `bash ./cmd.bash 24`
hit24 = load '$OUTPUT/JYMBII-batch/output/python-out-24/_files/Ztest$target24/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_24 `echo 24`
%declare echo2_24 `echo $target24`

%declare target25 `bash ./cmd.bash 25`
hit25 = load '$OUTPUT/JYMBII-batch/output/python-out-25/_files/Ztest$target25/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_25 `echo 25`
%declare echo2_25 `echo $target25`

%declare target26 `bash ./cmd.bash 26`
hit26 = load '$OUTPUT/JYMBII-batch/output/python-out-26/_files/Ztest$target26/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_26 `echo 26`
%declare echo2_26 `echo $target26`

%declare target27 `bash ./cmd.bash 27`
hit27 = load '$OUTPUT/JYMBII-batch/output/python-out-27/_files/Ztest$target27/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_27 `echo 27`
%declare echo2_27 `echo $target27`

%declare target28 `bash ./cmd.bash 28`
hit28 = load '$OUTPUT/JYMBII-batch/output/python-out-28/_files/Ztest$target28/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_28 `echo 28`
%declare echo2_28 `echo $target28`

%declare target29 `bash ./cmd.bash 29`
hit29 = load '$OUTPUT/JYMBII-batch/output/python-out-29/_files/Ztest$target29/test.out.hit' AS (memberId:int, jobId:int, Score:float);
%declare echo_29 `echo 29`
%declare echo2_29 `echo $target29`


hit = union hit0, hit1, hit2, hit3, hit4, hit5, hit6, hit7, hit8, hit9, hit10, hit11, hit12, hit13, hit14, hit15, hit16, hit17, hit18, hit19, hit20, hit21, hit22, hit23, hit24, hit25, hit26, hit27, hit28, hit29;

hit = filter hit by (Score < 100.0f and Score > -100.0f); 
 
hit = group hit by (memberId, jobId) parallel 50;
hit = foreach hit generate group.memberId as memberId, group.jobId as jobId, AVG(hit.Score) as score; 



-- Get the data of miss, i.e., the feature of a job is not available 

miss0 = load '$OUTPUT/JYMBII-batch/output/python-out-0/_files/Ztest$target0/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss1 = load '$OUTPUT/JYMBII-batch/output/python-out-1/_files/Ztest$target1/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss2 = load '$OUTPUT/JYMBII-batch/output/python-out-2/_files/Ztest$target2/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss3 = load '$OUTPUT/JYMBII-batch/output/python-out-3/_files/Ztest$target3/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss4 = load '$OUTPUT/JYMBII-batch/output/python-out-4/_files/Ztest$target4/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss5 = load '$OUTPUT/JYMBII-batch/output/python-out-5/_files/Ztest$target5/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss6 = load '$OUTPUT/JYMBII-batch/output/python-out-6/_files/Ztest$target6/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss7 = load '$OUTPUT/JYMBII-batch/output/python-out-7/_files/Ztest$target7/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss8 = load '$OUTPUT/JYMBII-batch/output/python-out-8/_files/Ztest$target8/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss9 = load '$OUTPUT/JYMBII-batch/output/python-out-9/_files/Ztest$target9/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss10 = load '$OUTPUT/JYMBII-batch/output/python-out-10/_files/Ztest$target10/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss11 = load '$OUTPUT/JYMBII-batch/output/python-out-11/_files/Ztest$target11/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss12 = load '$OUTPUT/JYMBII-batch/output/python-out-12/_files/Ztest$target12/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss13 = load '$OUTPUT/JYMBII-batch/output/python-out-13/_files/Ztest$target13/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss14 = load '$OUTPUT/JYMBII-batch/output/python-out-14/_files/Ztest$target14/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss15 = load '$OUTPUT/JYMBII-batch/output/python-out-15/_files/Ztest$target15/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss16 = load '$OUTPUT/JYMBII-batch/output/python-out-16/_files/Ztest$target16/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss17 = load '$OUTPUT/JYMBII-batch/output/python-out-17/_files/Ztest$target17/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss18 = load '$OUTPUT/JYMBII-batch/output/python-out-18/_files/Ztest$target18/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss19 = load '$OUTPUT/JYMBII-batch/output/python-out-19/_files/Ztest$target19/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss20 = load '$OUTPUT/JYMBII-batch/output/python-out-20/_files/Ztest$target20/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss21 = load '$OUTPUT/JYMBII-batch/output/python-out-21/_files/Ztest$target21/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss22 = load '$OUTPUT/JYMBII-batch/output/python-out-22/_files/Ztest$target22/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss23 = load '$OUTPUT/JYMBII-batch/output/python-out-23/_files/Ztest$target23/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss24 = load '$OUTPUT/JYMBII-batch/output/python-out-24/_files/Ztest$target24/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss25 = load '$OUTPUT/JYMBII-batch/output/python-out-25/_files/Ztest$target25/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss26 = load '$OUTPUT/JYMBII-batch/output/python-out-26/_files/Ztest$target26/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss27 = load '$OUTPUT/JYMBII-batch/output/python-out-27/_files/Ztest$target27/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss28 = load '$OUTPUT/JYMBII-batch/output/python-out-28/_files/Ztest$target28/test.out.miss' AS (memberId:int, jobId:int, Score:float);
miss29 = load '$OUTPUT/JYMBII-batch/output/python-out-29/_files/Ztest$target29/test.out.miss' AS (memberId:int, jobId:int, Score:float);


miss = union miss0, miss1, miss2, miss3, miss4, miss5, miss6, miss7, miss8, miss9, miss10, miss11, miss12, miss13, miss14, miss15, miss16, miss17, miss18, miss19, miss20, miss21, miss22, miss23, miss24, miss25, miss26, miss27, miss28, miss29;

miss = filter miss by (Score < 100.0f and Score > -100.0f); 
 
miss = group miss by (memberId, jobId) parallel 50;
miss = foreach miss generate group.memberId as memberId, group.jobId as jobId, AVG(miss.Score) as score; 


-- join hit and miss, if (memberId, jobId) is in hit, then use the score of hit, otherwise use the score of miss
data = join hit by (memberId, jobId) outer left, miss by (memberId, jobId);

SPLIT data into HIT if hit::memberId is not null, MISS if hit::memberId is null;

HIT = foreach HIT generate hit::memberId as memberId, hit::jobId as jobId, hit::score as score;
MISS = foreach MISS generate miss::memberId as memberId, miss::jobId as jobId, miss::score as score; 

data = union HIT, MISS; 

-- schema of test data is (class, memberId, jobId, score) 

test = load '$OUTPUT/JYMBII-batch/TMP/test' USING BinaryJSON();

-- test = foreach test generate sourceId as memberId, FLATTEN(hits);
-- test = foreach test generate memberId, hits::id as jobId, hits::score as score;

data = join test by (memberId, jobId) left outer, data by (memberId, jobId) parallel 50;

data = foreach data generate test::class as class, test::memberId as memberId, test::jobId as jobId, test::score as score, data::score as bc;

data = foreach data generate class, memberId, jobId, (bc is null ? score : (float)myudfs.logist(score, bc)) as score:float; 

data = foreach data generate memberId, (class, jobId, score) as hit;
data = group data by sourceId parallel 50;

data = foreach data generate (int)group as sourceId:int, data.hit as hits;
data = distinct data parallel 3;
store data into '$OUTPUT/JYMBII-batch/TMP/final-score' USING  BinaryJSON('intent','algorithmId','sourceId');

