#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : logit.py
#
# Purpose :
#
# Creation Date : 07-08-2013
#
# Last Modified : Wed 07 Aug 2013 11:41:53 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import java.lang.Math.exp
exp = java.lang.Math.exp

@outputSchema("score:double")
def logist(score, bc):
    x = score + bc 
    y = 1.0 / (1.0 + exp(-x))
    return y

