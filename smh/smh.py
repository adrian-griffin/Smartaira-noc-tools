import argparse
import os
import subprocess

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str)
args = parser.parse_args()

property = args.PropertyAbbreviation

errorNo = subprocess.run('ping -c 1 wea.smartaira360.com',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

print(errorNo.check_returncode())