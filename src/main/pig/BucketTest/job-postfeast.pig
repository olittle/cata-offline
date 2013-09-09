---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : score-pre.pig
--
-- Purpose : Generate the Job PostFeast to prepare the generation of job score 
--
-- Creation Date : 24-07-2013
--
-- Last Modified : Tue 06 Aug 2013 01:17:32 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

joblist = load '$OUTPUT/JYMBII-batch/TMP/history-data-collection' USING BinaryJSON();
joblist2 = load '$OUTPUT/JYMBII-batch/TMP/test-collection' USING BinaryJSON(); 

joblist = union joblist, joblist2; 

joblist = foreach joblist generate jobId;

joblist = distinct joblist parallel 10; 

jobPost = load '/data/derived/liar/grandfathering/jobs_postFeast/#LATEST' USING BinaryJSON(); 

-- job = join joblist by jobId, jobPost by id parallel 1000;
job = join jobPost by id, joblist by jobId using 'replicated';

job = foreach job generate jobPost::active as active, jobPost::deleted as deleted, jobPost::fields as fields, jobPost::id as id, jobPost::state as state, jobPost::type as type;

job = distinct job parallel 100;
 
store job into '$OUTPUT/JYMBII-batch/TMP/jobs_postFeast' USING BinaryJSON('id');  
 
