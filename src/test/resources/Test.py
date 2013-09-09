#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Test.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Tue 06 Aug 2013 02:40:45 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
import numpy as np 
#import matplotlib.pyplot as plt 

# Test the data based on Cost and Benefits 
def Test(Cost_array, Benefit_array, Member_array, K, f, TestData):
    
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
    
    Original = {} 
    Result = {}
   
    fout = open("test.result", "w")

    Score = np.zeros((len(TestData), 2))
    newScore = np.zeros((len(TestData), 2))

    index = 0
    tPos = 0
    tRrd = 0
    class_threshold = 1 

    for i in range(len(TestData)):
        vCla = TestData[i][0]
        memId = TestData[i][1]
        jobId = TestData[i][2] 
        vSc = TestData[i][3]

        if vCla < class_threshold:
            tPos += 1
        try:
            newScore[index, 0] =  vSc - Cost_array[memId] + np.dot( Benefit_array[jobId], Member_array[memId])
        except:
            print Cost_array[memId]
            print Benefit_array[jobId]
            print Member_array[memId]
            exit(1) 
#            newScore[index, 0] = beta[0] * vSc - 100 * Cost[memId] + 100 * Benefit[jobId]
        Score[index, 0] = vSc
        newScore[index, 1] = vCla
        Score[index, 1] = vCla
        index += 1
        fout.write(str(vCla) + "\t" + str(memId) + "\t" + str(jobId) + "\t" + str(vSc) + "\t" + str(newScore[index - 1, 0]) + "\n") 
    fout.close() 

    tRrd = index

    print "TestData Size", index 

# Rank Score
    newScore = sorted(newScore, key=lambda x:x[0], reverse = True)
    Score = sorted(Score, key=lambda x:x[0], reverse = True)

    newAUC_x = []
    newAUC_y = []

    AUC_x = []
    AUC_y = []

    newAUC_score = 0
    AUC_score = 0

    Pre = 0
    new_Pre = 0
    Rcl = 0
    new_Rcl = 0
    new_cPos = 0
    cPos = 0
    new_cPos = 0
    cTotal = 0
    lp = 0  
    lr = 0 
    lnp = 0 
    lnr = 0 

   # Study the orginal score and plot

    for i in range(tRrd):
        cTotal += 1
        if Score[i][1] < class_threshold:
            cPos += 1
        if newScore[i][1] < class_threshold:
            new_cPos += 1

        Pre = float(cPos) / float(cTotal)
        Rcl = float(cPos) / float(tPos)

        new_Pre = float(new_cPos) / float(cTotal)
        new_Rcl = float(new_cPos) / float(tPos)

        AUC_x.append(Rcl)
        AUC_y.append(Pre)

        newAUC_x.append(new_Rcl)
        newAUC_y.append(new_Pre)

        AUC_score += 0.5 * (lp + Pre) * (Rcl - lr)
        lp = Pre
        lr = Rcl

        newAUC_score += 0.5 * (lnp + new_Pre) * (new_Rcl - lnr)
        lnp = new_Pre
        lnr = new_Rcl
    
    print "Original Similarity, AUC = ", AUC_score
    print "new AUC score, AUC = ", newAUC_score
    
#    testfile = open("./test." + dataset + "." + str(f), "a") 
#    testfile.write(str(AUC_score) + "\t" + str(newAUC_score) + "\n")
#    testfile.close() 
    
    return newAUC_score

#    plt.plot(AUC_x, AUC_y, label = "origial similarity score, AUC = " + str(AUC_score))
#    plt.plot(newAUC_x, newAUC_y, label = "new score, AUC = " + str(newAUC_score))
#    plt.legend()
#    #plt.show()
#    plt.savefig("result.png")
