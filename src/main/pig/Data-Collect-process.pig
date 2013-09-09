---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Data-Collect-prep.pig
--
-- Purpose :
--
-- Creation Date : 08-08-2013
--
-- Last Modified : Thu 08 Aug 2013 03:20:24 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.


%declare target `./cmd.bash 1`
%declare echo `echo $target`
--data1 = load '$OUTPUT/JYMBII-batch/output-bak/python-out-1/_files/Ztest$target/test.out' AS (memberId:int, jobId:int, Score:double);
