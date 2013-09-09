#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Test.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Mon 09 Sep 2013 01:44:59 AM CDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 

# Test the data based on Cost and Benefits 
def Predict(Cost_array, Benefit_array, Member_array):
    
    job_index = {}
    mem_index = {}

    data = open("job.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        job_index[int(value[1])] = int(value[0]) 

    data = open("mem.index")
    for line in data:
        value = line.split("\n")[0].split("\t") 
        mem_index[int(value[1])] = int(value[0]) 
    
#    Global = 0
#    cnt = 0


    # Average the distrution of jobs in latent spaces 
    
    random_job = Benefit_array.sum(axis = 0) / Benefit_array.shape[0] 

    data = open("input.txt")
    for line in data:
        if line[0] != "p":
            continue 
        value = line.split("\n")[0].split("\t") 
        try:

            memId = mem_index[int(value[1])]
            jobId = job_index[int(value[2])]
            
#            Global += (np.dot(Benefit_array[jobId], Member_array[memId]))
#            cnt += 1

        except:
            pass 
  
#    Global = float(Global) / float(cnt)
#
#    print Global

    # jobs that appear in training dataset 
    fout_1 = open("./test.out.hit", "w")
    # jobs that never appear in training dataset 
    fout_2 = open("./test.out.miss", "w")

    data = open("input.txt")
    for line in data:
        if line[0] != "p":
            continue 
        value = line.split("\n")[0].split("\t")
       
        memId = int(value[1])
        jobId = int(value[2])

        if memId not in mem_index:
            continue
        
        memId = mem_index[memId]
        if jobId in job_index:
            jobId = job_index[jobId]
            newscore =  np.dot(Benefit_array[jobId], Member_array[memId]) - Cost_array[memId]
            fout_1.write(value[1] + "\t" + value[2] + "\t" + str(newscore) + "\n")

        else:
            newscore =  np.dot(random_job, Member_array[memId]) - Cost_array[memId]
            fout_2.write(value[1] + "\t" + value[2] + "\t" + str(newscore) + "\n")
            
    fout_1.close() 
    fout_2.close() 
   
