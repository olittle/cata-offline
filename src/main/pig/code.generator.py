#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : code.generator.py
#
# Purpose :
#
# Creation Date : 06-08-2013
#
# Last Modified : Tue 06 Aug 2013 05:43:25 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.

script = """
%declare target `./cmd.bash $INDEX`
data0 = load '/user/hgui/catastrophic-rec/python-out-$INDEX/test-$target/test.out' AS (memberId:int, jobId:int, Score:int);
"""
