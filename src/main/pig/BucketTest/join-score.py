
from org.apache.pig.scripting import Pig
import os 

if __name__ == "__main__":

    params = [] 
    
    
    prefix = "201306"
    for i in range(22, 31):
        day = prefix + str(i)
        par = {}
        par['DATE'] = day
        par['DD'] = str(i)
        par['MM'] = "06"
        params.append(par) 

    prefix = "201307"
    for i in range(1, 10):
        day = prefix + str(i)
        par = {}
        par['DATE'] = day
        par['DD'] = "0" + str(i)
        par['MM'] = "07"
        params.append(par) 
    
    prefix = "201307"
    for i in range(10, 26):
        day = prefix + str(i)
        par = {}
        par['DATE'] = day
        par['DD'] = str(i)
        par['MM'] = "07"
        params.append(par) 

    
    script = """

     score = load '/user/hgui/JYMBII-batch/history/mem-job-score-final' USING BinaryJSON();
--     %declare DIR 'delete'
--     data = load '/user/hgui/JYMBII-batch/history/$DIR/2013/$MM/$DD' USING BinaryJSON();
-- 
--     data = join score by (memberId, jobId), data by (memberId, jobId);
--     data = foreach data generate score::memberId as memberId, score::jobId as jobId, score::score as score; 
--     
--     store data into '/user/hgui/JYMBII-batch/history/$DIR/tmp-2013/$MM/$DD' USING BinaryJSON('memberId'); 
   
   ---------------------------------------------------------------------------------------------------------
    
    %declare DIR 'impression-inter-neg'
    data = load '/user/hgui/JYMBII-batch/history/$DIR/2013/$MM/$DD' USING BinaryJSON();
    data = join score by (memberId, jobId), data by (memberId, jobId) parallel 500;
    data = foreach data generate score::memberId as memberId, score::jobId as jobId, score::score as score;
    data = distinct data parallel 1; 
    store data into '/user/hgui/JYMBII-batch/history/$DIR/tmp-2013/$MM/$DD' USING BinaryJSON('memberId'); 
   ---------------------------------------------------------------------------------------------------------
    
    %declare DIR 'positive'
    data = load '/user/hgui/JYMBII-batch/history/$DIR/2013/$MM/$DD' USING BinaryJSON();
    data = join score by (memberId, jobId), data by (memberId, jobId) parallel 500;
    data = foreach data generate score::memberId as memberId, score::jobId as jobId, score::score as score; 
    data = distinct data parallel 1; 
    store data into '/user/hgui/JYMBII-batch/history/$DIR/tmp-2013/$MM/$DD' USING BinaryJSON('memberId'); 
   
   ---------------------------------------------------------------------------------------------------------

    %declare DIR 'view'
    data = load '/user/hgui/JYMBII-batch/history/$DIR/2013/$MM/$DD' USING BinaryJSON();
    data = join score by (memberId, jobId), data by (memberId, jobId) parallel 500; 
    data = foreach data generate score::memberId as memberId, data::time as time, score::jobId as jobId, score::score as score; 
    data = distinct data parallel 1; 
    store data into '/user/hgui/JYMBII-batch/history/$DIR/tmp-2013/$MM/$DD' USING BinaryJSON('memberId'); 
    """

    prog = Pig.compile(script) 
    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()
