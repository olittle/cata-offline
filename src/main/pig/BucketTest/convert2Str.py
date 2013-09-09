#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : convert2Str.py
#
# Purpose : Convert different schema into string 
#
# Creation Date : 03-08-2013
#
# Last Modified : Sat 03 Aug 2013 02:25:20 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

@outputSchema("str:chararray")
def TrainCnvrt2Str(label, vclass, memId, jobId, score):
    final = ""
    final += str(label) + "\t"
    final += str(vclass) + "\t"
    final += str(memId) + "\t"
    final += str(jobId) + "\t"
    final += str(score) 

    return final

@outputSchema("str:chararray")
def SeniorCnvrt2Str(label, memId, score):
    final = ""
    final += str(label) + "\t"
    final += str(memId) + "\t"
    final += str(score) 
    return final


def TestCnvrt2Str(label, memId, jobId, score):
    final = ""
    final += str(label) + "\t"
    final += str(memId) + "\t"
    final += str(jobId) + "\t"
    final += str(score) 

    return final
