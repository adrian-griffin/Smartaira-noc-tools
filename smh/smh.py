import argparse
import os
import subprocess
from sys import stdout

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str)
args = parser.parse_args()

PROPERTY_lower = args.PropertyAbbreviation
PROPERTY = str(PROPERTY_lower).upper()
test_domain = str(PROPERTY)+".smartaira360.com"


loganEdgeProperties = [
    'CBS','CCA','DCA','EHA','HSM','KKA','LAB','LOGAN OFFICE','NHA','OFA','OMV','OMVIEW','WRA'
]

if PROPERTY in loganEdgeProperties:
    VALID_DOMAIN = "logan.smartaira360.com"
else: 
    VALID_DOMAIN = PROPERTY+".smartaira360.com"


s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+VALID_DOMAIN+'' ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT)