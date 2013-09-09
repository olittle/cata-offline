---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : Split.pig
--
-- Purpose :
--
-- Creation Date : 28-07-2013
--
-- Last Modified : Thu 08 Aug 2013 04:41:02 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com)
--
--_._._._._._._._._._._._._._._._._._._._._.

register 'convert2Str.py' using jython as myudfs;

RMF $OUTPUT/JYMBII-batch/TMP/Buckets/Bucket-$INDEX


member = load '$OUTPUT/JYMBII-batch/TMP/MemList' USING BinaryJSON();
mem = sample member 0.25;

data = load '$OUTPUT/JYMBII-batch/TMP/history' USING BinaryJSON();

--
-- mem = foreach data generate memberId;
-- mem = distinct mem parallel 100;
--
-- mem = foreach mem generate memberId, RANDOM() as rand;
--
-- mem = filter mem by rand < 0.3;
--

data = join data by memberId, mem by memberId using 'replicated';

data = foreach data generate data::class as class, data::memberId as memberId, data::jobId as jobId, data::score as score;

data = foreach data generate class, memberId, jobId, score, RANDOM() as rand;
SPLIT data INTO training IF rand >= 0.1, testing IF rand < 0.1;

training = foreach training generate 't' as label, class, memberId, jobId, score;
testing = foreach testing generate 'c' as label, class, memberId, jobId, score;

data = union training, testing;

-- training and cv data
train = foreach data generate myudfs.TrainCnvrt2Str(label, class, memberId, jobId, score) as dta;

-- seniority data
senior = load '$OUTPUT/JYMBII-batch/TMP/Member-Senior-Score' USING BinaryJSON();
senior = foreach senior generate myudfs.SeniorCnvrt2Str(label, memberId, score) as dta;

-- test data
-- Schema of test data is (label, clas, memberId, jobId, score)    

test = load '$OUTPUT/JYMBII-batch/TMP/test' USING BinaryJSON();
test = foreach test generate myudfs.TestCnvrt2Str(label, memberId, jobId, score) as dta;

data = union train, senior, test;
data = distinct data parallel 1;

store data into '$OUTPUT/JYMBII-batch/TMP/Buckets/Bucket-$INDEX';
