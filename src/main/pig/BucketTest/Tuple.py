#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Tuple.py
#
# Purpose : Cacluate the Tuple Number for each member 
#
# Creation Date : 24-07-2013
#
# Last Modified : Wed 24 Jul 2013 01:21:27 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.


@outputSchema("Tuple:bag{(memberId:int, jobId_1:int, jobId_2:int)}") 
def Tuple_Construct(history):
    Member_Job_List = {}
    for i in range(4):
        Member_Job_List[i] = [] 

    for record in history:
        vClass = int(record[0])
        jobId = int(record[1])
        memId = int(record[2])
        Member_Job_List[vClass].append(jobId) 

    vPos = len(Member_Job_List[0]) 
    vView = len(Member_Job_List[1]) 
    vImpr = len(Member_Job_List[2]) 
    vDel = len(Member_Job_List[3]) 

    TupleSet = [] 

# 0 positive - null
    if vPos > 0:
        a = 0
        for i in range(len(Member_Job_List[a])):
            TupleSet.append((memId, Member_Job_List[a][i], -1))


# 1 positive - view 
    if vPos * vView > 0:
        a = 0
        b = 1 
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))
                
    
# 2 positive - impressed
    if vPos * vImpr > 0:
        a = 0
        b = 2 
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))
    
# 3 positive - deleted
    if vPos * vDel > 0:
        a = 0
        b = 3
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))
    
# 4 view - impressed
    if vView * vImpr > 0:
        a = 1
        b = 2 
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))

# ? view - null
    if vView > 0:
        a = 1
        for i in range(len(Member_Job_List[a])):
            TupleSet.append((memId, Member_Job_List[a][i], -1))
    
# 5 view - deleted
    if vView * vDel > 0:
        a = 1
        b = 3 
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))

# ? null - impressed
    if vImpr > 0:
        a = 2
        for i in range(len(Member_Job_List[a])):
            TupleSet.append((memId, -1, Member_Job_List[a][i]))

# 6 impressed - deleted
    if vImpr * vDel > 0:
        a = 2
        b = 3 
        for i in range(len(Member_Job_List[a])):
            for j in range(len(Member_Job_List[b])):
                TupleSet.append((memId, Member_Job_List[a][i], Member_Job_List[b][j]))
    
# 7 null - deleted
    if vDel > 0: 
        a = 3
        for i in range(len(Member_Job_List[a])):
            TupleSet.append((memId, -1, Member_Job_List[a][i]))
        
    return TupleSet   


if __name__ == "__main__":
    data = []
    data.append((0, 0, 1))
    data.append((1, 1, 1))
    data.append((2, 2, 1))
    data.append((3, 3, 1))
    print Tuple_Construct(data)

    
