import argparse
import os
import subprocess
import webbrowser

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str, help="Property abbreviation (ALNO, WEA, RRR, OPA, OMV, OMView, etc.)")

parser.add_argument('-c','--confluence', type=str, help="Open Confluence page for property")
parser.add_argument('-g','--graphical', type=str, help="Open Edge admin GUI page")

global args

args = parser.parse_args()

PROPERTY_lower = args.PropertyAbbreviation
PROPERTY = str(PROPERTY_lower)



loganEdgeProperties = [
    'CBS','CCA','DCA','EHA','HSM','KKA','LAB','LOGAN OFFICE','NHA','OFA','OMV','OMVIEW','WRA'
]

if PROPERTY in loganEdgeProperties:
    VALID_DOMAIN = "logan.smartaira360.com"
else: 
    VALID_DOMAIN = str(PROPERTY)+".smartaira360.com"


def sshProperty(VALID_DOMAIN):
    s = subprocess.run( [ 'ssh', ''+'agriffin'+'@'+VALID_DOMAIN+'' ])


def edgeGUIProperty(VALID_DOMAIN):
    url = "http://"+str(VALID_DOMAIN)+"/admin"
    webbrowser.open(url)


sshProperty(VALID_DOMAIN)