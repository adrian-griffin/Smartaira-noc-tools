import subprocess
import time

HOST=input("Edge IP/Domain: ")
PINGDESTINATION=input("Destination IP/Domain: ")
COUNT=input("Length of Test (seconds): ")
USER=input("RADIUS Username: ")
time.sleep(0.3)


def muteOutput():
    QUIETOPERATIONS=input("Mute Terminal Output? (y/n): ")
    if QUIETOPERATIONS == "y":
        muteBool = True
        print("Output Muted")
        print("")
    elif QUIETOPERATIONS == "n":
        muteBool = False
        print("Output Not Muted")
        print("")
    elif QUIETOPERATIONS == "N":
        muteBool = False
        print("Output Not Muted")
        print("")
    elif QUIETOPERATIONS == "Y":
        muteBool = True
        print("Output Muted")
        print("")
    else:
        print("")
        print("Please enter 'y' or 'n'!")
        muteOutput()
    return muteBool

muteResponseBool = muteOutput()

loc = str(HOST)+"_PINGTEST.txt"

print("")
print("")
print("------------------------------------------------------------------------------")
print("")

cmd_unmuted = "ssh "+USER+"@"+HOST+" 'ping -c "+COUNT+" "+PINGDESTINATION+" | while read pong; do echo \"$(date): $pong\"; done' | tee -i "+loc
cmd_muted = "ssh "+USER+"@"+HOST+" 'ping -q -c "+COUNT+" "+PINGDESTINATION+" | while read pong; do echo \"$(date): $pong\"; done' | tee -i "+loc

if muteResponseBool == True:
    temp = subprocess.run(cmd_muted, shell=True, check=True)
else:
    temp = subprocess.run(cmd_unmuted, shell=True, check=True)


print("")
print("")
print("")
print("")
print("")
print("")
print("------------------------------------------------------------------------------")
print("Ping test completed. Results saved to '"+loc+"'")
print("------------------------------------------------------------------------------")
print("")