###     NOTE: THIS SCRIPT WILL SOLELY CONVERT A .txt FILE OF IPs/ITEMS TO A .csv
####
#####   Convert a .txt Vertical List of IP Addresses (or any other items) TO A .csv
####
####    Flow: Parse IPList.txt >> Create Array of Items Based on Line-Breaks >> Create Vertical .csv of Items W/ Comma Separation
###
### Begin ###
###!! Importing depends
import os


###!! Checking script's current working directory
CWD_unsan = os.getcwd()
CWD_partial = CWD_unsan.replace("\\","/")
CWD = CWD_partial+"/"

###!! Defining and flushing dedicated Item/Address array
add_arr = []
add_arr.clear()

###!! Opening IPList.txt File for Reading
l = open(CWD+'IPList.txt','r')
###!! Creating && Opening SwitchHostIPs.csv File for Writing
c = open(CWD+'SwitchHostIPs.csv','w')

###!! Parsing IPList.txt file && Reading lines into array
address_lines = l.readlines()
for address in address_lines:
###!! Sanitizing array elems
    san_address = address.replace("\n","")
###!! Appending sanitized array elems to dedicated address array
    add_arr.append(san_address)
###!! Writing sanitized array elems from dedicated array to file with comma separation and newlines
    c.write(add_arr[0]+",\n")
###!! Clearing dedicated array to allow next item to be formatted
    add_arr.clear()

###!! Closing open files to prevent memory leakage or file access locks 
c.close()
l.close()