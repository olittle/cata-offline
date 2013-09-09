#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : LoadData.pyx
#
# Purpose : Load the Data and Create the index 
#
# Creation Date : 27-06-2013
#
# Last Modified : Tue 06 Aug 2013 05:18:19 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import random 
import math

import numpy as np 

def LoadData(f):

    # Load Different Relationship Data

    Member_Job_List = {} 
    Member_Job_Score = {}

    Cost = {}
    Cost_Prior = {} 

    Member = {} 
    Benefit = {}

    jobList = set()

# --------------------------------------------------------------
# May Change To different file formats
    paircnt = 0 

    data = open("input.txt") 
    for line in data:
        if line[0] != "t":
            continue 
        
        value = line.split("\n")[0].split("\t")
        vClass = int(value[1]) 
        memId = int(value[2])
        jobId = int(value[3])
        score = float(value[4])

        if memId not in Member_Job_List:
            Member_Job_List[memId] = {}
            for i in range(4):
                Member_Job_List[memId][i] = []  

        Member_Job_List[memId][vClass].append(jobId)
        Member_Job_Score[memId, jobId] = score 
        jobList.add(int(value[3]))
        paircnt += 1 
    print "paircnt", paircnt

# --------------------------------------------------------------

    memList = Member_Job_List.keys() 
    
    for memId in memList:
        Cost[memId] = 0
        Cost_Prior[memId] = 0 

    initMap = {}
    for i in range(12):
        initMap[i] = 1.0 / (1.0 + math.exp(0.5 * (1 - i))) - 0.5 

# Prior map between senior score and prior score 
# -------------------------------------------------------------
# Give prior and inital value for some members 
    
    data = open("input.txt")
    for line in data:
        if line[0] != "s":
            continue 

        value = line.split("\n")[0].split("\t")
        try:
            memId = int(value[1])
            if not memId in Cost:
                continue 
            score = int(value[2])
            Cost[memId] = initMap[score]
            Cost_Prior[memId] = initMap[score] 
        except:
            print line 

    for jobId in jobList:
        Benefit[jobId] = np.array(np.random.randn(f), dtype = np.float32)

    for memId in memList:
        Member[memId] = np.array(np.random.randn(f), dtype = np.float32) 
    
    # global Counter of relationship pairs

    gCounter = 0
    TupleSet = []
    Pos = []
    Neg = []

    for memId in memList:
        vPos = len(Member_Job_List[memId][0]) 
        vView = len(Member_Job_List[memId][1]) 
        vImpr = len(Member_Job_List[memId][2]) 
        vDel = len(Member_Job_List[memId][3]) 

# 0 positive - null
        if vPos > 0:
            gCounter += vPos
            a = 0
            for i in range(len(Member_Job_List[memId][a])):
                Pos.append((memId, Member_Job_List[memId][a][i], -1))

# 1 positive - view 
        if vPos * vView > 0:
            gCounter += vPos * vView
            a = 0
            b = 1 
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))
                    
        
# 2 positive - impressed
        if vPos * vImpr > 0:
            gCounter += vPos * vImpr
            a = 0
            b = 2 
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))
        
# 3 positive - deleted
        if vPos * vDel > 0:
            gCounter += vPos * vDel
            a = 0
            b = 3
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))
        
# 4 view - impressed
        if vView * vImpr > 0:
            gCounter += vView * vImpr
            a = 1
            b = 2 
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))

# ? view - null
        if vView > 0:
            gCounter += vView
            a = 1
            for i in range(len(Member_Job_List[memId][a])):
                Pos.append((memId, Member_Job_List[memId][a][i], -1))
        
# 5 view - deleted
        if vView * vDel > 0:
            gCounter += vView * vDel
            a = 1
            b = 3 
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))

# ? null - impressed
        if vImpr > 0:
            gCounter += vImpr 
            a = 2
            for i in range(len(Member_Job_List[memId][a])):
                Neg.append((memId, -1, Member_Job_List[memId][a][i]))

# 6 impressed - deleted
        if vImpr * vDel > 0:
            gCounter += vImpr * vDel
            a = 2
            b = 3 
            for i in range(len(Member_Job_List[memId][a])):
                for j in range(len(Member_Job_List[memId][b])):
                    TupleSet.append((memId, Member_Job_List[memId][a][i], Member_Job_List[memId][b][j]))
        
# 7 null - deleted
        if vDel > 0: 
            gCounter += vDel
            a = 3
            for i in range(len(Member_Job_List[memId][a])):
                Neg.append((memId, -1, Member_Job_List[memId][a][i]))

        
    Cost_array = np.array(np.random.randn(len(Cost)), dtype = np.float32)
    Cost_Prior_array =np.array( np.zeros(len(Cost)), dtype = np.float32) 
    Benefit_array = np.array(np.random.randn(len(Benefit), f), dtype = np.float32)
    Member_array = np.array(np.random.randn(len(Cost), f), dtype = np.float32) 

    job_index = {}
    index_job = {}
    mem_index = {}
    index_mem = {}

# Create index table for jobs 
    index = 0 
    for mem in Cost:
        mem_index[mem] = index
        index_mem[index] = mem 
        Cost_Prior_array[index] = Cost_Prior[mem]
        index += 1 

    index = 0 
    for job in Benefit:
        job_index[job] = index
        index_job[index] = job
        index += 1

    data = open("input.txt")
    TestData = []
    for line in data:
        if line[0] != "c":
            continue 
        value = line.split("\n")[0].split("\t") 
        try:
            vClass = int(value[1])
            memId = mem_index[int(value[2])]
            jobId = job_index[int(value[3])]
            score = float(value[4])
            TestData.append([vClass, memId, jobId, score])

        except:
            pass 

    fout = open("job.index", "w")

    for i in index_job:
        fout.write(str(i) + "\t" + str(index_job[i]) + "\n")
    fout.close() 
    
    fout = open("mem.index", "w")
    for i in index_mem:
        fout.write(str(i) + "\t" + str(index_mem[i]) + "\n")
    fout.close() 
    
    TupleSet_array = np.zeros((len(TupleSet), 6), dtype = np.float32)
    Pos_array = np.zeros((len(Pos), 4), dtype = np.float32)
    Neg_array = np.zeros((len(Neg), 4), dtype = np.float32) 

    for i in range(len(TupleSet)):
        u = TupleSet[i][0]
        j1 = TupleSet[i][1]
        j2 = TupleSet[i][2]

        s1 = Member_Job_Score[u, j1]
        j1 = job_index[j1] 

        s2 = Member_Job_Score[u, j2]
        j2 = job_index[j2]

        u = mem_index[u] 
        TupleSet_array[i] = np.array([i, u, j1, j2, s1, s2], dtype = np.float32)
    
    for i in range(len(Pos)):
        u = Pos[i][0]
        j1 = Pos[i][1]
        s1 = Member_Job_Score[u, j1]

        j1 = job_index[j1] 
        u = mem_index[u] 
        Pos_array[i] = np.array([i + len(TupleSet), u, j1, s1], dtype  = np.float32)
    
    for i in range(len(Neg)):
        u = Neg[i][0]
        j2 = Neg[i][2]
        s2 = Member_Job_Score[u, j2]

        j2 = job_index[j2]
        u = mem_index[u] 
        Neg_array[i] = np.array([i + len(TupleSet) + len(Pos), u, j2, s2], dtype  = np.float32)
   
    # Reduce the memory needed 
    Cost_array = np.array(Cost_array, dtype = np.float32)
    Cost_Prior_array = np.array(Cost_Prior_array, dtype = np.float32) 
    Benefit_array = np.array(Benefit_array, dtype = np.float32) 
    Member_array = np.array(Member_array, dtype = np.float32)
    TestData = np.array(TestData, dtype = np.float32) 

    TupleSet_array = np.array(TupleSet_array, dtype  = np.float32) 
    Pos_array = np.array(Pos_array, dtype  = np.float32) 
    Neg_array = np.array(Neg_array, dtype  = np.float32)
  
    return Cost_array, Cost_Prior_array, Benefit_array, Member_array, TestData, TupleSet_array, Pos_array, Neg_array

if __name__ == "__main__":
    LoadData(32)
