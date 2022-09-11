import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str)
args = parser.parse_args()

PROPERTY = args.PropertyAbbreviation

try:
    s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+PROPERTY+'.smartaira360.com' ])
except:
    try: 
        s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+PROPERTY+'.bluerim.net' ])
    except:
        s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+'logan'+'.smartaira360.com' ])
