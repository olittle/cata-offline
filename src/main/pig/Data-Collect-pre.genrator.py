#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Data-Collect-pre.genrator.py
#
# Purpose :
#
# Creation Date : 08-08-2013
#
# Last Modified : Thu 08 Aug 2013 09:49:28 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.


script = """
%default folder@ /tmp/python-out-@
%declare rm@ `rm -rf $folder@`
%declare e@ `mkdir $folder@`

fs -copyToLocal /user/haliu/JYMBII-batch/output/python-out-@/m* $folder@
"""

fout = open("Data-Collect-prep.pig", "w")
for i in range(30):
    new = script.replace("@", str(i))
    fout.write(new) 

fout.close() 
