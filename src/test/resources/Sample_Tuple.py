#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Sample_Tuple.pyx
#
# Purpose : Sample 3000 random tuples from the dataset 
#
# Creation Date : 27-06-2013
#
# Last Modified : Mon 22 Jul 2013 11:14:47 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import random 
import bisect 

def Sample_Tuple(Member_Job_List, Member_inverted_index, gTupleCnt, aCounter):

    # Generate random number between (0, gTupleCnt)
    arrTuple = []  
    for vItr in range(30000):
        vRandom = random.randint(1, gTupleCnt) - 1
        
        s = Member_inverted_index[aCounter[bisect.bisect_left(aCounter, vRandom)]]
        memId = s[0]
        iType_1 = s[1]
        iType_2 = s[2] 

        if iType_1 != -1:
            jId_1 = random.sample(Member_Job_List[memId][iType_1], 1)[0] 
        else:
            jId_1 = -1

        if iType_2 != -1:
            jId_2 = random.sample(Member_Job_List[memId][iType_2], 1)[0]
        else:
            jId_2 = -1
        
        if jId_1 == -1 and jId_2 == -1:
            print "Error Generating Update Tuple"
            exit(1) 

        iTuple = (memId, jId_1, jId_2) 
        arrTuple.append(iTuple)

    return arrTuple

