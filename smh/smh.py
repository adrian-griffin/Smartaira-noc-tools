import argparse
import os
import time
import subprocess
import sys
import webbrowser
import configparser

import contextlib
import io

parser = argparse.ArgumentParser(description="SSH into an Edge using only the property abbreviation (eg. smh alno)")
parser.add_argument("PropertyAbbreviation", type=str, help="Property abbreviation (ALNO, WEA, LOGANOFFICE, OPA, OMV, OMView, etc.)")


parser.add_argument('-c','--confluence', action="store_true", help="Open Confluence page for property")
parser.add_argument('-g','--graphical', action="store_true", help="Open Edge admin GUI page in webbrowser")

global SSHBOOL
global args


CWD_unsan = os.getcwd()
CWD_partial = CWD_unsan.replace("\\","/")
CWD = CWD_partial+"/"
config = configparser.ConfigParser()
config.read(CWD+'credentials.ini')
config.sections()


#RADIUS_PASSWORD = EDGEHOSTNAME=str(config['RADIUS_CREDENTIALS']['RadiusPassword'])
RADIUS_USERNAME = EDGEHOSTNAME=str(config['RADIUS_CREDENTIALS']['RadiusUsername'])

SSHBOOL = True


def sshProperty(VALID_DOMAIN):
    s = subprocess.run( [ 'ssh', ''+str(RADIUS_USERNAME)+'@'+VALID_DOMAIN+'' ])


def edgeGUIProperty(VALID_DOMAIN):
    url = "http://"+str(VALID_DOMAIN)+"/admin"
    webbrowser.open(url,0,True)    
    os._exit(0)



args = parser.parse_args()

PROPERTY_lower = args.PropertyAbbreviation
PROPERTY = str(PROPERTY_lower).upper()



loganEdgeProperties = [
    'CBS','CCA','DCA','EHA','HSM','KKA','LAB','LOGANOFFICE','NHA','OFA','OMV','OMVIEW','WRA'
]

if PROPERTY in loganEdgeProperties:
    VALID_DOMAIN = "logan.smartaira360.com"
else: 
    VALID_DOMAIN = str(PROPERTY)+".smartaira360.com"

if args.graphical:
    edgeGUIProperty(VALID_DOMAIN)

if SSHBOOL == True:
    sshProperty(VALID_DOMAIN)

