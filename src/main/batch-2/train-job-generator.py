#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : train-job-generator.py
#
# Purpose : Generate the job automatically
#
# Creation Date : 28-07-2013
#
# Last Modified : Thu 29 Aug 2013 06:28:13 PM CDT
#
# Created By : Huan Gui (hgui@linkedin.com)
#
#_._._._._._._._._._._._._._._._._._._._._.

pylib = '/jobs/tictac/lib'
script = """
type=java
job.class=com.linkedin.metronome.common.mapred.Executor

dependencies=upload-resources

cache.archive-python=$PYLIB/python-2.7.5-metronome.jar
cache.archive-lapack=$PYLIB/lapack-3.2.1-metronome.jar

cache.file-Test.py=${home.dir}/resources/Test.py
cache.file-Sample_Tuple.py=${home.dir}/resources/Sample_Tuple.py
cache.file-LoadData.py=${home.dir}/resources/LoadData.py
cache.file-main-mem-reduce.py=${home.dir}/resources/main-mem-reduce.py
cache.file-Store.py=${home.dir}/resources/Store.py
cache.file-lr_solver_BC.py=${home.dir}/resources/lr_solver_BC.py
cache.file-lr_solver_MC.py=${home.dir}/resources/lr_solver_MC.py
cache.file-Predict.py=${home.dir}/resources/Predict.py

cache.file-input.txt=${data.dir}/Bucket-@


command-test0=python/bin/python main-mem-reduce.py 32 250 8
output.files-test0=test.out.hit,test.out.miss


command-test1=python/bin/python main-mem-reduce.py 32 250 8
output.files-test1=test.out.hit,test.out.miss


command-test2=python/bin/python main-mem-reduce.py 32 250 8
output.files-test2=test.out.hit,test.out.miss


command-test3=python/bin/python main-mem-reduce.py 32 250 8
output.files-test3=test.out.hit,test.out.miss


command-test4=python/bin/python main-mem-reduce.py 32 250 8
output.files-test4=test.out.hit,test.out.miss


command-test5=python/bin/python main-mem-reduce.py 32 250 8
output.files-test5=test.out.hit,test.out.miss


command-test6=python/bin/python main-mem-reduce.py 32 250 8
output.files-test6=test.out.hit,test.out.miss


command-test7=python/bin/python main-mem-reduce.py 32 250 8
output.files-test7=test.out.hit,test.out.miss


command-test8=python/bin/python main-mem-reduce.py 32 250 8
output.files-test8=test.out.hit,test.out.miss


command-test9=python/bin/python main-mem-reduce.py 32 250 8
output.files-test9=test.out.hit,test.out.miss


env-PATH=python/bin:/usr/local/bin:/usr/bin
env-PYTHONPATH=./:python/lib/python2.7/site-packages
env-LD_LIBRARY_PATH=lapack:python/lib:/usr/local/lib:/usr/lib

# Change output.path to somewhere you have write access.
output.path=${output.dir}/python-out-@

hadoop-conf.mapred.job.reduce.memory.mb=7168
hadoop-conf.mapred.task.timeout=36000000
"""

script = script.replace("$PYLIB", pylib)
print script

for i in range(30):
    fout = open("./train-" + str(i) + ".job", "w")
    new_script = script.replace("@", str(i))
    print new_script
    fout.write(new_script)
    fout.close()

fout = open("dummy.job", "w")
fout.write("""
type=command
command=echo
""")
script = """
dependencies=train-0"""
fout.write(script)
for i in range(1, 30):
    fout.write(",train-" + str(i))
fout.close()

