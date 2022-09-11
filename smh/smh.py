import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str)
args = parser.parse_args()

PROPERTY = args.PropertyAbbreviation

test_domain = str(PROPERTY)+".smartaira360.com"

p = subprocess.run( [ 'ping', '-c 1 -s 1 -q', str(test_domain) ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
if int(p.returncode) < 2:
    VALID_DOMAIN = ".smartaira360.com"
else: 
    VALID_DOMAIN = ".bluerim.net"


s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+PROPERTY+VALID_DOMAIN+'' ])
