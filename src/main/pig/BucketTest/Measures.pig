---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Measures.pig
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

register 'measurements.py' using jython as myudfs;
define AVG org.apache.pig.builtin.AVG();

data  = load '$OUTPUT/JYMBII-batch/TMP/final-score' USING  BinaryJSON();

--  use pig udf to calculate AUC (Personalized AUC for each member)
result = foreach data generate sourceId, myudfs.metrics(hits) as metric;
result = group result all; 
result = foreach result generate  "BC-Model"as method,  AVG(metric.AUC) as AUC, AVG(metric.AUPR) as AUPR, AVG(metric.Pre_1) as Pre_1, AVG(metric.Pre_3) as Pre_3, AVG(metric.Pre_10) as Pre_10, AVG(metric.NDCG_1) as NDCG_1, AVG(metric.NDCG_3) as NDCG_3, AVG(metric.NDCG_10) as NDCG_10; 
 

data  = load '$OUTPUT/JYMBII-batch/TMP/test' USING  BinaryJSON();

--  use pig udf to calculate AUC (Personalized AUC for each member)
result2 = foreach data generate sourceId, myudfs.metrics(hits) as metric;
result2 = group result2 all; 
result2 = foreach result2 generate  "JYMBII"as method,  AVG(metric.AUC) as AUC, AVG(metric.AUPR) as AUPR, AVG(metric.Pre_1) as Pre_1, AVG(metric.Pre_3) as Pre_3, AVG(metric.Pre_10) as Pre_10, AVG(metric.NDCG_1) as NDCG_1, AVG(metric.NDCG_3) as NDCG_3, AVG(metric.NDCG_10) as NDCG_10; 

result = union result, result2; 
 
store result into '$OUTPUT/JYMBII-batch/TMP/measurements' USING BinaryJSON();  
