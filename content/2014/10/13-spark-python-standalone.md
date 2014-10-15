Title: Spark 1.1 and standalone Python scripts
Tags: spark, python
Category: Tech
comments: enabled
Slug: spark1-1_python_standalone
Summary: Spark 1.1 was released a few weeks ago, and I've been curious about using it from a standalone Python script.  While Spark has Java and Scala bindings, the Python one appeals to me most--I'd really like to be able to use Spark from within a standalone Python script, and then step through it in PyCharm, which is the IDE I really enjoy.  Here's how to do that on Mac OS X 10.9

The Github repo for this is here: https://github.com/danlmarmot/demo-spark1.1-python

## Install Spark
We're going to install Spark in ~/bin/spark from pre-built versions on Apache.  You already should've installed Java--this post assumes an Oracle version of Java.

Open a Terminal window, then run these commands:

    mkdir -p ~/bin/spark; cd $_
    wget http://d3kbcqa49mib13.cloudfront.net/spark-1.1.0-bin-hadoop2.4.tgz
    tar -zxvf spark-1.1.0-bin-hadoop2.4.tgz; ln -s spark-1.1.0-bin-hadoop2.4 current; cd current
    bin/pyspark
    
Note that I'm putting Spark as a symlink at ~/bin/spark/current, to allow for any scripts I create to reference a fixed location for Spark.

### Turn down Spark's logging verbosity

Spark's logging spews out a lot.  Turn it down with these two commands:

    cd ~/bin/spark/current
    cp conf/log4j.properties.template conf/log4j.properties
    sed -i'' -e 's/log4j.rootCategory=INFO/log4j.rootCategory=WARN/g' conf/log4j.properties

Yes, that sed one-liner looks odd but this is a Mac with BSD sed, and not GNU sed.


## Add your first Python script

This first script goes through and simply counts the number of lines with a's and b's in the Spark 1.1 Read Me.  It's not dependent on anything other than the Spark install location.

Create a new file called readme_count_ab.py, and dump this text into it:


```
#!/usr/bin/env python

# Run this with either python readme_count_ab.py, or ./readme_count_ab.py

import sys, os

SPARK_HOME = os.path.join(os.environ["HOME"], "bin/spark/current/")
sys.path.append(os.path.join(SPARK_HOME, "python"))
sys.path.append(os.path.join(SPARK_HOME, "python/lib/py4j-0.8.2.1-src.zip"))

from pyspark import SparkContext

read_me = os.path.join(SPARK_HOME, "README.md")
sc = SparkContext("local", "Read Me")
read_me_data = sc.textFile(read_me).cache()

numAs = read_me_data.filter(lambda s: 'a' in s).count()
numBs = read_me_data.filter(lambda s: 'b' in s).count()

print "Lines with a: %i, lines with b: %i" % (numAs, numBs)

# A couple of assertions to make sure things are correct
assert(numAs is 83)
assert(numBs is 38)
```

Run this with ./readme_count_ab.py


## Add a second Python script - the word count

This next script also uses Spark to count words in the ReadMe.txt.  Go ahead and create a new file called readme_word_count.py, with this text inside:

```
#!/usr/bin/env python
__author__ = 'dmckean'

'''
    Run this with either python readme_word_count.py, or ./readme_word_count.py
'''

import os
import sys
from pprint import pprint


SPARK_HOME = os.path.join(os.environ["HOME"], "bin/spark/current/")
sys.path.append(os.path.join(SPARK_HOME, "python"))
sys.path.append(os.path.join(SPARK_HOME, "python/lib/py4j-0.8.2.1-src.zip"))
from pyspark import SparkContext

sc = SparkContext("local", "Read Me")
read_me_data = sc.textFile(os.path.join(SPARK_HOME, "README.md")).cache()

counts = read_me_data.flatMap(lambda line: line.split(" "))\
    .map(lambda word: (word, 1))\
    .reduceByKey(lambda a, b: a + b)

word_counts = counts.collect()
pprint(word_counts)
```

Run this with ./readme_count_words.py or python readme_count_words.py

This second script will print out a list of all 166 words in the Read Me.
Note that the data isn't really cleaned up--there are punctuation and other things included as part of each word.  That 
cleanup is best left for another exercise; after all, so much of big data stuff is just cleaning up the input data!


