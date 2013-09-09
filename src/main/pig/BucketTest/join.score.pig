---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : join.score.pig
--
-- Purpose :
--
-- Creation Date : 27-07-2013
--
-- Last Modified : Sat 27 Jul 2013 11:59:00 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

%declare DIR 'positive'
score = load '$OUTPUT/JYMBII-batch/history/mem-job-score-final' USING BinaryJSON();
data = load '$OUTPUT/JYMBII-batch/history/$DIR/2013/$MM/$DD' USING BinaryJSON();

data = join score by (memberId, jobId), data by (memberId, jobId);
data = foreach data generate score::memberId as memberId, score::jobId as jobId, score::score as score; 

store data into '$OUTPUT/JYMBII-batch/history/$DIR/tmp-2013/$MM/$DD' USING BinaryJSON("memberId"); 

