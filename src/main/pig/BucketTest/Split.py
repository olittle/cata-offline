#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Split.py
#
# Purpose :
#
# Creation Date : 28-07-2013
#
# Last Modified : Mon 29 Jul 2013 02:04:11 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.


from org.apache.pig.scripting import Pig
import os 

if __name__ == "__main__":

    bucket = 10 

    params = [] 
    
    for i in range(bucket):
        par = {} 
        par['INDEX'] = str(i)
        params.append(par) 

    
    script = """
        data = load '/user/hgui/JYMBII-batch/TMP/history' USING BinaryJSON(); 

        mem = foreach data generate memberId;
        mem = distinct mem parallel 100;

        mem = sample mem 0.5; 

        data = join data by memberId, mem by memberId; 

        data = distinct data parallel 1; 

        data = foreach data generate data::label as label, data::class as class, data::memberId as memberId, data::jobId as jobId, data::score as score; 
        store data into '/user/hgui/JYMBII-batch/TMP/bucket-$INDEX';

    """

    prog = Pig.compile(script)

    for para in params:
        bound = prog.bind(para) 
        stats = bound.runSingle()
