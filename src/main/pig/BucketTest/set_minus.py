#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : set_minus.py
#
# Purpose : Define the minus operation 
#
# Creation Date : 20-06-2013
#
# Last Modified : Sun 28 Jul 2013 02:05:27 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

@outputSchema("negs:bag{(jobId:int)}") 
def Constraints2(bag, const_1, const_2):
    const_set = set() 
    for x in const_1:
        y = x[0]
        const_set.add(y)
    for x in const_2:
        y = x[0]
        const_set.add(y)

    new_bag = [] 

    for x in bag:
        y = x[0]
        if y not in const_set:
            new_bag.append((y, )) 

    return new_bag


@outputSchema("negs:bag{(jobId:int)}") 
def Constraints3(bag, const_1, const_2, const_3):
    const_set = set() 
    
    for x in const_1:
        y = x[0]
        const_set.add(y)
    
    for x in const_2:
        y = x[0]
        const_set.add(y)
    
    for x in const_3:
        y = x[0]
        const_set.add(y)

    new_bag = [] 

    for x in bag:
        y = x[0]
        if y not in const_set:
            new_bag.append((y, )) 

    return new_bag
