#-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : input.py
#
# Purpose :
#
# Creation Date : 30-07-2013
#
# Last Modified : Tue 30 Jul 2013 06:18:39 PM PDT
#
# Created By : Huan Gui (hgui@linkedin.com) 
#
#_._._._._._._._._._._._._._._._._._._._._.


script = """
#Job properties
type=pig
dependencies=jymbii-batch-senority,jymbii-batch-test$ALL_SPLIT
hadoop.job.ugi=${hadoop.job.ugi.cmd}
udf.import.list=oink.:com.linkedin.pig.:com.linkedin.pig.date.:org.apache.pig.piggybank.:org.apache.pig.piggybank.evaluation.:org.apache.pig.piggybank.evaluation.string.:org.apache.pig.piggybank.evaluation.math.:com.linkedin.liar.pigUDFs.
#pig.additional.jars=${project.artifactId}-${project.version}.jar

pig.script=./BucketTest/input.py
# Arguments for optimizing Pig on Hadoop
#jvm.args=-Dmapred.job.queue.name=marathon -Djava.io.tmpdir=/grid/a/mapred/tmp -Ddfs.umaskmode=002 -Dpig.additional.jars=${pig.home}/lib/*:./${project.artifactId}-${project.version}.jar
jvm.args=-Djava.io.tmpdir=/grid/a/mapred/tmp -Ddfs.umaskmode=002 -Dpig.additional.jars=${pig.home}/lib/*:./${project.artifactId}-${project.version}.jar

# Azkaban parameters
azkaban.should.proxy=${azkaban.should.proxy}
user.to.proxy=${user.to.proxy}
hdfs.default.classpath.dir=${remote.library.path}
classpath=${local.classpath}

param.DIR=Aggregate
"""
splits = ""
for i in range(100):
    splits += "," + "jymbii-batch-split-" + str(i)


new = script.replace("$ALL_SPLIT", splits)

fout = open("../jymbii-batch-input.job", "w")
fout.write(new)
fout.close()

