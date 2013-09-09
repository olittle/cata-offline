#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : measurements.py
#
# Purpose : Calculate different measurements including AUC, AUPR, NDCG @ 3, Precision @ 3
#
# Creation Date : 05-09-2013
#
# Last Modified : Thu 05 Sep 2013 07:08:52 PM CDT
#
# Created By : Huan Gui (huangui2@illinois.edu) 
#
#_._._._._._._._._._._._._._._._._._._._._.

from java.lang.Math import log 

def metrics(hits):

    # sorted the hit list by BC score or jymbii score  
    scores = sorted(hits, key=lambda x:x[2], reverse='True')
    print scores
    score = 0 

    total = len(hits) 
    AUC = 0
    
    N = 0 
    P = 0 
    for i in range(total):
        # applied 
        if hits[i][0] == 0:
            P += 1 
        else:
            N += 1
  
    # No Click for this members, just remove the member from measurements.  
    if P == 0:
        return -1 


################################### AUC #######################################
    TP = 0 
    FP = 0
    TPR = 0 
    FPR = 0
    TPR_last = 0 
    FPR_last = 0 
    AUC = 0 

    for i in range(total):
        if scores[i][0] == 0:
            TP += 1
        else:
            FP += 1

        TPR = float(TP) / float(P)
        FPR = float(FP) / float(N) 
        AUC += 0.5 * (FPR - FPR_last) * (TPR + TPR_last) 

        TPR_last = TPR
        FPR_last = FPR


################################### AUPR ######################################

    relevant = 0 
    retrieved = 0
    Pre = 0
    Pre_last = 0 
    Rec = 0 
    Rec_last = 0 
    AUPR = 0 

    for i in range(total):
        if scores[i][0] == 0:
            relevant += 1
        retrieved += 1 

        Pre = float(relevant) / float(retrieved)
        Rec = float(relevant) / float(P) 
        AUPR += 0.5 * (Rec - Rec_last) * (Pre + Pre_last) 

        Pre_last = Pre
        Rec_last = Rec

################################### Precision @ 1 ######################################

    k = 1
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if scores[i][0] == 0:
            correct += 1
    Pre_1 = float(correct) / float(i+1) 

################################### Precision @ 3 ######################################

    k = 3 
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if scores[i][0] == 0:
            correct += 1
    Pre_3 = float(correct) / float(i+1) 
        

################################### Precision @ 10 ######################################

    k = 10 
    correct = 0 
    for i in range(k):
        if i > total:
            break 
        if scores[i][0] == 0:
            correct += 1
    Pre_10 = float(correct) / float(i+1) 


################################### NDCG @ 1 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 1 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if scores[i][0] == 0:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_1 = DCG / IDCG


################################### NDCG @ 3 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 3 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if scores[i][0] == 0:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_3 = DCG / IDCG 


################################### NDCG @ 10 ######################################

    # define Zn so that perfect ranking have NDCG = 1 
   
    k = 10 
    DCG = 0 
    IDCG = 0 
    for i in range(k):
        if i > total:
            break
    
        if scores[i][0] == 0:
            DCG += log(2) / log(i + 2)  
        
    x = P
    if P > k:
        x = k 
    for i in range(x):
        IDCG += log(2) / log(i + 2) 
    
    NDCG_10 = DCG / IDCG 
    
    return AUC, AUPR, Pre_1, Pre_3, Pre_10,  NDCG_1, NDCG_3, NDCG_10


data = [(0, 1, 0.342), (1, 2, 0.387), (1, 3, 0.2445), (1, 2, 0.327), (0, 3, 0.23445), (3, 2, 0.087), (2, 3, 0.4445), (1, 2, 0.3087), (0, 3, 0.92445), (1, 2, 0.34487), (1, 3, 0.52445)]

print metrics(data) 


