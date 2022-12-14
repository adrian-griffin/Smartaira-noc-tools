###
####
#####   Execute Telnet Commands Over SSH Jump-Host
####
####    Flow: SSH into an Edge (or any other jump-host) >> Remote execute a Telnet tunnel from the Edge to any device on the internal network >>
####    >> Remote execute a series of commands over Telnet over SSH >> Save output file on Edge >> Copy file data to local machine >> 
####    >> Clean output file from Edge
###
### Begin ###
###!! Importing depends
import paramiko
import time
import random
import string
import configparser
import os


###!! Checking script's current working directory
CWD_unsan = os.getcwd()
CWD_partial = CWD_unsan.replace("\\","/")
CWD = CWD_partial+"/"

###!! Gathering EDGE/RADIUS, TP-Link, and local machine login credentials
config = configparser.ConfigParser()
#config.read(CWD+'credentials.ini')
config.read('C:/Users/AdrianGriffin/Documents/GitHub/Smartaira-noc-tools/TelnetCMDsOverSSH/credentials.ini')
config.sections()

EDGEHOSTNAME=str(config['EDGE_CREDENTIALS']['EdgeHostname'])
RADIUSUSERNAME=str(config['EDGE_CREDENTIALS']['RadiusUsername'])
RADIUSPASSWORD=str(config['EDGE_CREDENTIALS']['RadiusPassword'])

DESTINATIONHOSTNAME=str(config['DESTINATION_CREDENTIALS']['DestinationHostname'])
DESTINATIONUSERNAME=str(config['DESTINATION_CREDENTIALS']['DestinationUsername'])
DESTINATIONPASSWORD=str(config['DESTINATION_CREDENTIALS']['DestinationPassword'])

SSHPORT=int(config['PORT_OPTIONS']['SSHPort'])
TELNETPORT=int(config['PORT_OPTIONS']['TelnetPort'])

###!! Initiating SSH tunnel into Edge or other jumphost
EDGETUNNEL = paramiko.SSHClient()
###!! Setting policy to be used if connection to Edge/jumphost does not have an already known SSH key
EDGETUNNEL.set_missing_host_key_policy(paramiko.AutoAddPolicy())
EDGETUNNEL.connect(EDGEHOSTNAME, username=RADIUSUSERNAME, password=RADIUSPASSWORD)



######!! BEGIN: Optional block for adding another intermediate jump between the Edge/Jump1 and the final destination
'''
JUMPHOST_Generic = paramiko.SSHClient()
JUMPHOST_Generic.set_missing_host_key_policy(paramiko.AutoAddPolicy())
JUMPHOST_Generic.connect(JUMPHOSTGEN_HOSTNAME, username=JUMPHOSTGEN_USERNAME, password=JUMPHOSTGEN_PASSWORD, sock=EDGETUNNEL_NewChannel)
'''
######!! END


#####!! BEGIN:  Remote telnet command execution pipes any and all data that comes through the CLI into a file on the Edge. Data is read from the file and processed locally,
#       where it is then deleted off of the Edge. To be safe and ensure that this program will never delete any important files off of the Edge due to the same file name
#       a random, 32 character title is generated each time. Better safe than sorry.
#####!! END

OutputFileTitle = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(30))

###!! Initiating Telnet tunnel into destination host/TP-Link && Creating variables to pass STDIN, STDOUT, and STDERR data into. Data is tee'd into a random file name.
stdin, stdout, stderr = EDGETUNNEL.exec_command("telnet "+DESTINATIONHOSTNAME+" | tee -i "+OutputFileTitle+"jumphost.out")


###!! Passing login credentials through the outer SSH tunnel's STDIN to be then passed into Telnet tunnel
###!! Program waits 1.3 seconds before entering the Username and Password to ensure that it doesn't enter the credentials before the connection can be established
###!! Passing final destination Username + newline char to simulate an 'Enter' keypress
#stdin.write(""+str(DESTINATIONUSERNAME)+'''\n\n''')
###!! Passing final destination Password + newline char to simulate an 'Enter' keypress
#stdin.write(""+str(DESTINATIONPASSWORD)+'''\n\n''')

import tplinkcommands

stdin.write(str(DESTINATIONUSERNAME)+'''
'''+str(DESTINATIONPASSWORD)+tplinkcommands.telnet_command_str)
time.sleep(3)

stdin.close()


###!! Copying the output file data from the Edge to local machine
stdin, stdout, stderr = EDGETUNNEL.exec_command("cat "+OutputFileTitle+"jumphost.out")

o = open(CWD+OutputFileTitle+'jumphost.out','w')
output_lines = stdout.readlines()
###!! Writing data from Edge to local machine
for outline in output_lines:
    o.write(outline)

time.sleep(2)
###!! Deleting the output file, and only the output file, from the Edge.
EDGETUNNEL.exec_command("rm "+OutputFileTitle+"jumphost.out")
#


###!! Closing STDIN - Post output copy to local machine && removal of file on Edge
stdin.close()

###!! Closing connection to the optional block for adding another intermediate jump between the Edge/Jump1 and the final destination
#JUMPHOST_Generic.close()

###!! Closing SSH tunnel to the Edge
EDGETUNNEL.close()


### End ###
