---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : member-job-score.pig
--
-- Purpose : Get the score of member AND jobs 
--
-- Creation Date : 27-06-2013
--
-- Last Modified : Thu 27 Jun 2013 09:55:08 AM PDT
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

STORE data INTO '$OUTPUT/JYMBII/rawscore.2/' USING BinaryJSON('memberId');   
