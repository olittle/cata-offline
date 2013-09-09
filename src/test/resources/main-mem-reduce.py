#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : main.py
#
# Purpose : The main module for algorithm to calculate the absolute cost / benefits of members / companies 
#
# Creation Date : 27-06-2013
#
# Last Modified : Thu 08 Aug 2013 04:23:22 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from LoadData import LoadData
from Store import Store
from Test import Test
from time import time 
import sys
from Predict import Predict
from scipy.sparse import lil_matrix, csr_matrix, csc_matrix 

from lr_solver_BC import lr_solver_BC
from lr_solver_MC import lr_solver_MC
import numpy as np

if __name__ == "__main__":

    f = int(sys.argv[1]) 
    inLoop = int(sys.argv[2])
    outLoop = int(sys.argv[3]) 

    # Read Data 
    start = time()  
    Cost_array, Cost_Prior_array, Benefit_array, Member_array, TestData, TupleSet_array, Pos_array, Neg_array = LoadData(f)

    Tuple_len = len(TupleSet_array) 
    Pos_len = len(Pos_array) 
    Neg_len = len(Neg_array)

    memCnt = len(Member_array) 
    jobCnt = len(Benefit_array) 
    
    print "job partial order, pos order, neg order", Tuple_len, Pos_len, Neg_len
    print "memCnt, jobCnt", memCnt, jobCnt

    gTupleCnt = Tuple_len + Pos_len + Neg_len 
    
    print "Tuple Count", gTupleCnt
    print time() - start    
    start = time() 
    trainSize = gTupleCnt
    b = np.zeros((trainSize, 1), dtype = np.float32)
    print time() - start 
    start = time() 

    trIndex = 0 
    # Input the tuple data
    for i in range(Tuple_len):
        iTuple = TupleSet_array[i]  
        sim_1 = iTuple[4]
        sim_2 = iTuple[5]
        
        b[trIndex, 0] = sim_1 - sim_2 
        trIndex += 1 
    
    # Input the Pos data
    for i in range(Pos_len):
        iTuple = Pos_array[i]  
        sim_1 = iTuple[3]
        
        b[trIndex, 0] = sim_1 
        trIndex += 1 

    # Input the Neg data 
    for i in range(Neg_len):
        iTuple = Neg_array[i]  
        sim_2 = iTuple[3]
        
        b[trIndex, 0] = - sim_2 
        trIndex += 1 
    
    TupleSet_array = np.array(TupleSet_array[:, :4], dtype = np.int) 
    Pos_array = np.array(Pos_array[:, :3], dtype = np.int) 
    Neg_array = np.array(Neg_array[:, :3], dtype = np.int) 
   
    A_BC_x = np.array([], dtype = np.int)
    A_BC_y = np.array([], dtype = np.int) 


    for k in range(f):
        A_BC_x = np.concatenate((A_BC_x, np.array(TupleSet_array[:, 0], dtype = np.int), np.array(TupleSet_array[:, 0], dtype = np.int), np.array(Pos_array[:, 0], dtype = int), np.array(Neg_array[:, 0], dtype = np.int)))
        A_BC_y = np.concatenate((A_BC_y, np.array(TupleSet_array[:, 2] * f + k, dtype = np.int), np.array(TupleSet_array[:, 3] * f + k, dtype = np.int), np.array(Pos_array[:, 2] * f + k, dtype = np.int), np.array(Neg_array[:, 2] * f + k, dtype = np.int)))
        
    A_BC_x = np.concatenate((A_BC_x, np.array(Pos_array[:, 0], dtype = np.int)))
    A_BC_y = np.concatenate((A_BC_y, np.array(Pos_array[:, 1] + jobCnt * f, dtype = np.int)))
        
    A_BC_x = np.concatenate((A_BC_x, np.array(Neg_array[:, 0], dtype = np.int)))
    A_BC_y = np.concatenate((A_BC_y, np.array(Neg_array[:, 1] + jobCnt * f, dtype = np.int)))
    
    
    A_MC_x = np.array([], dtype = np.int)
    A_MC_y = np.array([], dtype = np.int) 

    for k in range(f):
        A_MC_x = np.concatenate((A_MC_x, np.array(TupleSet_array[:, 0], dtype = np.int), np.array(Pos_array[:, 0], dtype = np.int), np.array(Neg_array[:, 0], dtype = np.int)))
        A_MC_y = np.concatenate((A_MC_y, np.array(TupleSet_array[:, 1] * f + k, dtype = np.int), np.array(Pos_array[:, 1] * f + k, dtype = np.int), np.array(Neg_array[:, 1] * f + k, dtype = np.int)))

    A_MC_x = np.concatenate((A_MC_x, np.array(Pos_array[:, 0], dtype = np.int)))
    A_MC_y = np.concatenate((A_MC_y, np.array(Pos_array[:, 1] + memCnt * f, dtype = np.int)))
        
    A_MC_x = np.concatenate((A_MC_x, np.array(Neg_array[:, 0], dtype = np.int)))
    A_MC_y = np.concatenate((A_MC_y, np.array(Neg_array[:, 1] + memCnt * f, dtype = np.int)))
    
    print time() - start
    
    
    vUpdate = 3000

    uCnt = -1 

    # Temp Cost and Benefits for parallelism

    print "start training ..............................."
    
    Best_AUPR = 0 
    stepsize = 0.001

    while vUpdate > 100 and uCnt < outLoop:
        
        uCnt += 1

        p_array = {}
        
        innerUpdate = inLoop 

        Member_array, Cost_array, update2 = lr_solver_MC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, Cost_Prior_array, A_MC_x, A_MC_y, innerUpdate, stepsize)
        Benefit_array, Cost_array, update1 = lr_solver_BC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, A_BC_x, A_BC_y, innerUpdate, stepsize)
       
        print "Update ", uCnt, update1, update2
        # Store the Model
    
        newAUC_score = Test(Cost_array, Benefit_array, Member_array, uCnt, f, TestData)

        if newAUC_score > Best_AUPR:
            Best_AUPR = newAUC_score
            Store(Cost_array, Benefit_array, Member_array, uCnt, f)

    Predict(Cost_array, Benefit_array, Member_array)
    print "new AUC score, AUC = ", Best_AUPR
