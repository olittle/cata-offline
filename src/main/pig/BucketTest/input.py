#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : input.py
#
# Purpose :
#
# Creation Date : 26-07-2013
#
# Last Modified : Tue 06 Aug 2013 09:08:04 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

import os 
from org.apache.pig.scripting import Pig

# Move the file into input directory

if __name__ == "__main__":
    
    bucket = 30 
    for index in range(bucket):
        os.system("hadoop dfs -rmr -skipTrash /user/hgui/JYMBII-batch/input/input-" + str(index) + ".txt")
        os.system("hadoop dfs -cp /user/hgui/JYMBII-batch/TMP/Buckets/Bucket-" + str(index) + "/part-r-00000 /user/hgui/JYMBII-batch/input/input-" + str(index) + ".txt")
