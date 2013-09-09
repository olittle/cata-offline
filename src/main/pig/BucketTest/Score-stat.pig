---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Tuple.pig
--
-- Purpose : Generate Tuples for each members 
--
-- Creation Date : 24-07-2013
--
-- Last Modified : Wed 07 Aug 2013 09:49:02 AM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

register 'Tuple.py' using jython as myfuncs; 

define AVG org.apache.pig.builtin.AVG();

score = load '$OUTPUT/JYMBII-batch/history/member-job-score' USING BinaryJSON('date.range','num.days=5;days.ago=0;error.on.missing=false');
score = foreach score generate sourceId as memberId, FLATTEN(hits);
score = foreach score generate memberId, hits::id as jobId, hits::score as score;
score = group score by (memberId, jobId) parallel 1000;
score = foreach score generate group.memberId as memberId, group.jobId as jobId, AVG(score.score) as score; 

pos = load '$OUTPUT/JYMBII-batch/TMP/positive' USING BinaryJSON();
del = load '$OUTPUT/JYMBII-batch/TMP/delete' USING BinaryJSON();
view = load '$OUTPUT/JYMBII-batch/TMP/view_no_click' USING BinaryJSON();
impr = load '$OUTPUT/JYMBII-batch/TMP/impr_no_view' USING BinaryJSON(); 

pos = join score by (memberId, jobId), pos by (memberId, jobId) parallel 5000;
pos = foreach pos generate pos::class as class, pos::memberId as memberId, pos::jobId, score::score as score;   
pos = group pos all;
pos = foreach pos generate 'pos', COUNT(pos) as cnt;  


del = join score by (memberId, jobId), del by (memberId, jobId) parallel 5000;
del = foreach del generate  del::class as class, del::memberId as memberId, del::jobId, score::score as score;   
del = group del all;
del = foreach del generate 'del', COUNT(del) as cnt;  


view = join score by (memberId, jobId), view by (memberId, jobId) parallel 5000;
view = foreach view generate view::class as class, view::memberId as memberId, view::jobId, score::score as score;   
view = group view all;
view = foreach view generate 'view', COUNT(view) as cnt;  

impr = join score by (memberId, jobId), impr by (memberId, jobId) parallel 5000;
impr = foreach impr generate  impr::class as class, impr::memberId as memberId, impr::jobId, score::score as score;   
impr = group impr all;
impr = foreach impr generate 'impr', COUNT(impr) as cnt;  

data = union pos, del, view, impr;

dump data;
