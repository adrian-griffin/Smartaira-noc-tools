###            
####
#####   Scan For and Gather Info About Any Device Connected to a TP-Link Switch at a Property
####
####    Flow: Parse SwitchHostIPs.csv >> Execute 'TelnetCMDsOverSSH' >> Scan each Host with LLDP Neighbours >> 
####    >> Detect all appearances of a specified device on all listed Hosts >> Return .csv file with data of each appearance
###
### Begin ###
###!! Importing depends
import re
import paramiko
import time
import random
import string
import configparser
import os
import re
import csv

###!! Checking script's current working directory
CWD_unsan = os.getcwd()
CWD_partial = CWD_unsan.replace("\\","/")
CWD = CWD_partial+"/"


###!! Defining and flushing dedicated Item/Address array
address_array = []
address_array.clear()

###!! Parsing SwitchHostIPs.csv 
c = open(CWD+'SwitchHostIPs.csv','r')
address_lines = c.readlines()

###!! Joining .csv data into array to be stored in memory
for address in address_lines:
    address_san = address.replace(",\n","")
    address_array.append(address_san)


###!! Gathering EDGE/RADIUS, TP-Link, and desired device to scan
config = configparser.ConfigParser()
config.read(CWD+'credentials.ini')
config.sections()

EDGEHOSTNAME=config['EDGE_CREDENTIALS']['EdgeHostname']
RADIUSUSERNAME=config['EDGE_CREDENTIALS']['RadiusUsername']
RADIUSPASSWORD=config['EDGE_CREDENTIALS']['RadiusPassword']

DESTINATIONUSERNAME=config['DESTINATION_CREDENTIALS']['DestinationUsername']
DESTINATIONPASSWORD=config['DESTINATION_CREDENTIALS']['DestinationPassword']

SSHPORT=int(config['PORT_OPTIONS']['SSHPort'])
TELNETPORT=int(config['PORT_OPTIONS']['TelnetPort'])

DEVICENAME=config['DEVICE_TO_SCAN']['DeviceToScan']


###!! Initiating SSH tunnel into Edge or other jumphost
EDGETUNNEL = paramiko.SSHClient()
###!! Setting policy to be used if connection to Edge/jumphost does not have an already known SSH key
EDGETUNNEL.set_missing_host_key_policy(paramiko.AutoAddPolicy())
EDGETUNNEL.connect(EDGEHOSTNAME, username=RADIUSUSERNAME, password=RADIUSPASSWORD)


def connectToSecondaryDevice(DESTINATIONHOSTNAME):
    ###!! Retreiving Edge transport object for Edge SSH to be used at a lower level (opening a new channel)
    EDGETUNNEL_Transport = EDGETUNNEL.get_transport()
    ###!! Declaring new vars for defining destination/final host params (The TP-Link Switch(es) in this case)
    Dest_addr_TRANSPORT = (DESTINATIONHOSTNAME, SSHPORT)
    Local_addr_TRANSPORT = (EDGEHOSTNAME, SSHPORT)
    ###!! Opening new channel using the local-to-Edge SSH transport object that reaches out to the final destination
    EDGETUNNEL_NewChannel = EDGETUNNEL_Transport.open_channel("direct-tcpip", Dest_addr_TRANSPORT, Local_addr_TRANSPORT)


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
    stdin, stdout, stderr = EDGETUNNEL.exec_command("telnet "+DESTINATIONHOSTNAME+" | tee -i "+OutputFileTitle+"velvet.out")


    ###!! Passing login credentials through the outer SSH tunnel's STDIN to be then passed into Telnet tunnel
    ###!! Program waits 1.3 seconds before entering the Username and Password to ensure that it doesn't enter the credentials before the connection can be established
    time.sleep(1.3)
    ###!! Passing final destination Username + newline char to simulate an 'Enter' keypress
    stdin.write(DESTINATIONUSERNAME+"\n")
    time.sleep(1.3)
    ###!! Passing final destination Password + newline char to simulate an 'Enter' keypress
    stdin.write(DESTINATIONPASSWORD+"\n")
    time.sleep(1.3)
    ###!! Reading desired commands from tplinkcommands.txt
    stdin.write("\n")
    f = open(CWD+'tplinkcommands.txt','r')
    command_lines = f.readlines()
    ###!! Passing desired commands into Telnet terminal from STDIN
    for command in command_lines:
        stdin.write(command)

    ###!! Closing STDIN - Post destination command execution
    stdin.write("exit\n")
    stdin.close()


    ###!! Copying the output file data from the Edge to local machine
    stdin, stdout, stderr = EDGETUNNEL.exec_command("cat "+OutputFileTitle+"velvet.out")

    o = open(CWD+OutputFileTitle+'velvet.out','w')
    output_lines = stdout.readlines()
    ###!! Writing data from Edge to local machine
    for outline in output_lines:
        o.write(outline)

    time.sleep(2)
    ###!! Deleting the output file, and only the output file, from the Edge.
    EDGETUNNEL.exec_command("rm "+OutputFileTitle+"velvet.out")
    #


    ###!! Closing STDIN - Post output copy to local machine && removal of file on Edge
    stdin.close()
    returnedFileName = OutputFileTitle+"velvet.out"
    return returnedFileName

###!! Analyzing LLDP Neighbor Information 
def returnedLLDPNeighborAnalyzer(returnedLLDPData):

    DEVICENAME=config['DEVICE_TO_SCAN']['DeviceToScan']

    ###!! Declaring and flushing arrays for device occurrences and the grabbed MAC Address of the device

    occ_arr = []
    occ_arr.clear()

    found_arr = []
    found_arr.clear()

    MAC_ARR = []
    MAC_ARR.clear()
    
    
    LLDPData = returnedLLDPData
    ###!! Regex to find occurrences of the device name within the entire returned output file
    occ_arr = [m.start() for m in re.finditer(DEVICENAME, str(LLDPData))]
    ###!! Appending MAC Address array with every MAC of specified device found
    for occ_index in occ_arr:
        MAC_ARR.append(found_arr.append(LLDPData[occ_index:occ_index+17]))
    # # # # # # # # # # # # # # # # # # ^^^ Needs to be changed to correctly reflext the MAC location
    # # # H510 34:8F:27:16:4F:A0 | MAC is 17 chars long

    return MAC_ARR


for address in address_array:
    ###!! Calls Telnet & Output generation function, saves to variable
    returnedLLDPData = connectToSecondaryDevice(str(address))
    ###!! Calls Output Analyzer to locate occurrences and find MAC Addresses, saves to variable
    MAC_ARR = returnedLLDPNeighborAnalyzer(returnedLLDPData)
    ###!! 'i' variable is used to iterate through MAC Address array for every positive hit for specified device
    i=0
    if len(MAC_ARR) != 0:
        ###!! If MAC array is not empty, writes to the output .csv file with corresponding data
        with open("ResultData.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str(address),"TRUE","TRUE",DEVICENAME+" "+MAC_ARR[i]])
        i += 1
    else: 
        ###!! If MAC array is indeed empty, writes to the output .csv file with corresponding data
        with open("ResultData.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([str(address),"TRUE","",""])





###!! Closing connection to the optional block for adding another intermediate jump between the Edge/Jump1 and the final destination
#JUMPHOST_Generic.close()

###!! Closing SSH tunnel to the Edge
EDGETUNNEL.close()


### End ###