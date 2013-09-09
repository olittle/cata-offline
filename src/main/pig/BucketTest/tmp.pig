---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : tmp.pig
--
-- Purpose :
--
-- Creation Date : 30-07-2013
--
-- Last Modified : Tue 30 Jul 2013 05:33:19 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

data = load '$OUTPUT/JYMBII-batch/history/delete/2013/07/29-1' USING BinaryJSON();

member = load '$OUTPUT/JYMBII-batch/TMP/memList' USING BinaryJSON();
data = join data by memberId, member by memberId;
data = foreach data generate data::memberId as memberId, data::jobId as jobId, data::time as time; 

STORE data INTO '$OUTPUT/JYMBII-batch/history/delete/2013/07/29' USING BinaryJSON('memberId'); 
