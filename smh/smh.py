import argparse
import os
import time
import subprocess
import sys
import webbrowser
import configparser

import contextlib
import io

## Hi

global RADIUS_PASSWORD
global RADIUS_USERNAME

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str, help="Property abbreviation (ALNO, WEA, OPA, OMV, OMView, etc.)")


parser.add_argument('-c','--confluence', action="store_true", help="Open Confluence page for property")
parser.add_argument('-g','--graphical', action="store_true", help="Open Edge admin GUI page in webbrowser")

global SSHBOOL
global args


CWD_unsan = os.getcwd()
CWD = CWD_unsan.replace("\\","/")

config = configparser.ConfigParser()
config.read('~/NOC_Radius_Credentials.ini')
config.sections()

SSHBOOL = True
RADIUS_PASSWORD = config['RADIUS_CREDENTIALS']['RadiusUsername']
RADIUS_USERNAME = config['RADIUS_CREDENTIALS']['RadiusPassword']


def sshProperty(VALID_DOMAIN):
    s = subprocess.run( [ 'ssh', ''+str(RADIUS_USERNAME)+'@'+VALID_DOMAIN+'' ])

    
def edgeGUIProperty(VALID_DOMAIN):
    url = "http://"+str(VALID_DOMAIN)+"/admin"
    webbrowser.open(url,0,True)    
    os._exit(0)



args = parser.parse_args()

PROPERTY_lower = args.PropertyAbbreviation
PROPERTY = str(PROPERTY_lower).upper()

VALID_DOMAIN = str(PROPERTY)+".smartaira360.com"

if args.graphical:
    edgeGUIProperty(VALID_DOMAIN)

if SSHBOOL == True:
    sshProperty(VALID_DOMAIN)

