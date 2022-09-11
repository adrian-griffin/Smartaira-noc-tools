import argparse
import os
import subprocess
from sys import stdout

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str)
args = parser.parse_args()

PROPERTY = args.PropertyAbbreviation

test_domain = str(PROPERTY)+".smartaira360.com"

p = subprocess.run( [ 'ping', '-c 1 -s 1 -q', str(test_domain) ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
if int(p.returncode) < 1:
    VALID_DOMAIN = PROPERTY+".smartaira360.com"
else: 
    VALID_DOMAIN = "logan.smartaira360.com"


s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+VALID_DOMAIN+'' ],
    stdout=subprocess.STDOUT,
    stderr=subprocess.STDOUT)