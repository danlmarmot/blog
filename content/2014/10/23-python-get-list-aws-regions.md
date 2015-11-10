Title: Listing AWS regions with Python
Tags: python, aws
Category: tech
comments: enabled
Slug: python-get-list-aws-regions
Summary: A short snippet of Python code to get the current list of AWS regions

With Amazon's announcement of the new Frankfurt AWS region (eu-central-1), I've gone back and reworked several old 
Python scripts that had AWS region lists hardcoded in them.

This tiny snippet code is a handly oneliner.  You can just run it as a Python file, or from the command line. 

It does require the Python package boto version 2.34.0 (update, Oct 2015: this doesn't work with Amazon's newer boto3 library).

Both versions of the code also strip out the China region and the US Govcloud region (I don't have services in either location) and the
list is sorted as well.

####print_aws_regions.py

Uses Python 2 or 3 and boto

```python
from __future__ import print_function
from boto import ec2

REGIONS = sorted([r.name for r in ec2.regions() if r.name not in ["cn-north-1", "us-gov-west-1"]])

for r in REGIONS:
    print(r)
```


#### Command Line with boto

You can also just spit out a list of current AWS regions from the command line.  This uses system Python, which is almost always Python 2.
  
```bash
python -c 'from boto import ec2;REGIONS = sorted([r.name for r in ec2.regions() if r.name not in ["cn-north-1", "us-gov-west-1"]]); print REGIONS'
```