---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
--
-- File Name : score-inputGenerator.pig
--
-- Purpose : Generate the mem 
--
-- Creation Date : 30-07-2013
--
-- Last Modified : Sun 04 Aug 2013 03:43:07 PM PDT
--
-- Created By : Huan Gui (hgui@linkedin.com) 
--
--_._._._._._._._._._._._._._._._._._._._._.

data = LOAD '/data/derived/liar/grandfathering/members_postFeast/#LATEST'  USING BinaryJSON();
data = foreach data generate id, type, deleted, active, fields, txn, profile_targeting_data, member_std_data_avro; 


job = LOAD '$OUTPUT/JYMBII-batch/TMP/history-data-collection' USING BinaryJSON();
job = foreach job generate memberId, (int)jobId as jobId;
 
jobgrp = group job by memberId;
jobgrp = foreach jobgrp generate group as memberId, job.jobId as jobIds; 
 
data = join data by id, jobgrp by memberId using 'replicated';
 
-- generate filterList for Crown
data = foreach data generate data::id as id, data::txn as txn, data::type as type, data::deleted as deleted, data::active as active, data::fields as fields, jobgrp::jobIds as filterList, data::profile_targeting_data as profile_targeting_data, data::member_std_data_avro as member_std_data_avro;

data = distinct data parallel 50; 

store data into '$OUTPUT/JYMBII-batch/TMP/member-postfeast' USING BinaryJSON('id');
