#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : temp.py
#
# Purpose :
#
# Creation Date : 06-08-2013
#
# Last Modified : Tue 06 Aug 2013 04:55:56 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.i

fout = open("1-input.txt", "w")
data = open("input.txt")

for line in data:
    if line[0] == "c" or line[0] == "t" or line[0] == "s":
        fout.write(line) 

fout.close() 

