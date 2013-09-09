
data = load '$OUTPUT/JYMBII-batch/history/delete/2013/07/25/' USING BinaryJSON();
score = load '$OUTPUT/JYMBII-batch/history/mem-job-score-final' USING BinaryJSON();

data = join data by (memberId, jobId), score by (memberId, jobId);
data = foreach data generate score::memberId as memberId, score::jobId as jobId, score::score as score; 

store data into  '$OUTPUT/JYMBII-batch/history/delete/tmp-2013/07/25/' USING BinaryJSON('memberId');

