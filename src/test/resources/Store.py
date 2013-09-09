#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Store.pyx
#
# Purpose :
#
# Creation Date : 28-06-2013
#
# Last Modified : Tue 06 Aug 2013 02:35:39 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
def Store(Cost_array, Benefit_array, Member_array, k, f):
    
    cost_fout = open("Member.Cost" , "w") 
    for memId in range(len(Cost_array)):
        cost_fout.write(str(memId) + "\t" + str(Cost_array[memId]) + "\n")
    cost_fout.close()
    
    bene_fout = open("Job.Benefit.Matrix" , "w") 
    for jobId in range(len(Benefit_array)):
        bene_fout.write(str(jobId) + "\t")
        for j in range(f):
            bene_fout.write(str(Benefit_array[jobId][j]) + " ") 
        bene_fout.write("\n")
    bene_fout.close() 

    bene_fout = open("Member.Benefit.Matrix", "w") 
    for memId in range(len(Member_array)):
        bene_fout.write(str(memId) + "\t")
        for j in range(f):
            bene_fout.write(str(Member_array[memId][j]) + " ") 
        bene_fout.write("\n")
    bene_fout.close()

