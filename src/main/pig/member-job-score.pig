---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : member-job-score.pig
--
-- Purpose : Get the score of member AND jobs 
--
-- Creation Date : 27-06-2013
--
-- Last Modified : Sun 28 Jul 2013 03:56:28 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

data = LOAD '$OUTPUT/member_job_score/scores/' USING BinaryJSON();
data = FOREACH data GENERATE sourceId, hits; 
data = FILTER data BY not IsEmpty(hits); 
data = FOREACH data GENERATE sourceId AS memberId, FLATTEN(hits);

data = FOREACH data GENERATE memberId, hits::id AS jobId, hits::score AS score; 

STORE data INTO '$OUTPUT/JYMBII/rawscore/' USING BinaryJSON('memberId');   



data = LOAD '$OUTPUT/member_job_score/scores.2' USING BinaryJSON();
data = FOREACH data GENERATE sourceId, hits; 
data = FILTER data BY not IsEmpty(hits); 
data = FOREACH data GENERATE sourceId AS memberId, FLATTEN(hits);

data = FOREACH data GENERATE memberId, hits::id AS jobId, hits::score AS score; 
data = distinct data parallel 10; 

STORE data INTO '$OUTPUT/JYMBII/rawscore.2/' USING BinaryJSON('memberId');   
