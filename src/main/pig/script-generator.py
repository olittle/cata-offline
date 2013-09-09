#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : script-generator.py
#
# Purpose :
#
# Creation Date : 31-07-2013
#
# Last Modified : Wed 31 Jul 2013 01:35:20 AM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
##_._._._._._._._._._._._._._._._._._._._._.

fout = open("Data-Collect.pig", "w")
fout.write("define AVG org.apache.pig.builtin.AVG();\n")

script = """
%declare target `./cmd.bash $INDEX`
data_$INDEX = load '/user/hgui/JYMBII-batch/output/_files/test-$target/test.out' AS (memberId:int, jobId:int, Score:int);
"""
for i in range(30):
    new = script.replace("$INDEX", str(i)) 
    fout.write(new)

join = "data = join data_0"
for i in range(1, 30):
    join += ", data_" + str(i)
join += ";\n"

fout.write(join) 

script = """

data = group data by (memberId, jobId);
data = foreach data generate group.memberId as memberId, group.jobId as jobId, AVG(data.Score) as score; 

test = load '/user/hgui/JYMBII-batch/history/member-job-score/' USING BinaryJSON('date.range'; 'num.days=1');

"""
