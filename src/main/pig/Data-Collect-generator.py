#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : Data-Collect-generator.py
#
# Purpose :
#
# Creation Date : 07-08-2013
#
# Last Modified : Fri 09 Aug 2013 08:36:46 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

script = """
%declare target$INDEX `bash ./cmd.bash $INDEX`
data$INDEX = load '$OUTPUT/JYMBII-batch/output/python-out-$INDEX/_files/Ztest$target$INDEX/test.out' AS (memberId:int, jobId:int, Score:float);
%declare echo_$INDEX `echo $INDEX`
%declare echo2_$INDEX `echo $target$INDEX`
"""

new = ""

for i in range(30):
    x = script.replace("$INDEX", str(i)) 
    new += x

union = "data = union data0"
for i in range(1, 30):
    union += ", data" + str(i) 

fout = open("Data-Collect.pig.bak", "w")
fout.write(new)
fout.write(union + ";\n") 

print new
fout.close()
