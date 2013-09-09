#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : lr_solver_BC.pyx
#
# Purpose :
#
# Creation Date : 16-07-2013
#
# Last Modified : Thu 08 Aug 2013 04:19:59 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from scipy.sparse import lil_matrix, csr_matrix, csc_matrix, coo_matrix 
import numpy as np
from time import time 

def lr_solver_BC(TupleSet_array, Pos_array, Neg_array, Cost_array, Benefit_array, Member_array, b, A_x, A_y, innerUpdate, stepsize):

#    np.seterr(all = 'raise') 
    trIndex = 0

    jobCnt, f = Benefit_array.shape
    memCnt = len(Member_array)

    dimension = jobCnt * f + memCnt
    
    Tuple_len = len(TupleSet_array) 
    Pos_len = len(Pos_array) 
    Neg_len = len(Neg_array) 

    trainSize = Tuple_len + Pos_len + Neg_len  
    start = time() 
    
    x = np.zeros((dimension, 1), dtype = np.float32) 
    # Build the x value 
    for i in range(jobCnt):
        for k in range(f):
            x[i * f + k, 0] = Benefit_array[i, k] 

    for i in range(memCnt):
        x[jobCnt * f + i, 0] = Cost_array[i]

#    b = lil_matrix((trainSize, 1), dtype = float32)

    A_data = np.array([], dtype = np.float32)
    for k in range(f):
        A_data = np.concatenate((A_data, Member_array[TupleSet_array[:, 1]][:, k], -1 * Member_array[TupleSet_array[:, 1]][:, k], Member_array[Pos_array[:, 1]][:, k], -1 * Member_array[Neg_array[:, 1]][:, k]))
    A_data = np.concatenate((A_data, -1 * np.ones(Pos_len, dtype = np.float32)))
    A_data = np.concatenate((A_data, np.ones(Neg_len, dtype = np.float32)))

    A = coo_matrix((A_data, (A_x, A_y)), shape = ((trainSize, dimension)), dtype = np.float32)
   
    del A_data 
    
    A = csr_matrix(A, dtype = np.float32) 

    print time() - start 

    update = trainSize 
    alpha = stepsize 
    regular = 1 
    
    start = time() 

    z = x.copy()
    for k in range(innerUpdate):
        x_p  = x

        AxPb = (A.dot(z) + b)
        prob = 1.0 / (1.0 + np.exp(AxPb))
        update_arr = A.T.dot(prob)
        update_arr = update_arr - regular * z 
        
        x = z + alpha *( update_arr)
        z = x + k/(k+3.0) * (x - x_p)

    opt = np.log(1.0 / (1.0 + np.exp(-1 * AxPb))).sum() - 0.5 * regular * np.square(x).sum()
    print "update B,c", time() - start,  opt  

    # Convert x back into array 
    
    for i in range(jobCnt):
        for k in range(f):
            Benefit_array[i, k] = x[i * f + k, 0] 

    for i in range(memCnt):
        Cost_array[i] = x[jobCnt * f + i, 0] 

    return Benefit_array, Cost_array, opt 
