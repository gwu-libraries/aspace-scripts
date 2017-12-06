

#Import modules and configuration files.
import json
import requests
import secrets #secrets.py is a file that should be in the same directory as this file
import configs #configs.py is a file that should be in the same directory as this file
import datetime
import csv
import argparse

#Set up argparse so that the script can take arguments in the terminal.
parser = argparse.ArgumentParser(description="Retrieve metadata about digital objects in ArchivesSpace. Requires a text file with list of digital object ArchivesSpace UIDs.")
parser.add_argument("input", help="path to text file with list of digital object UIDs", required=True)
parser.add_argument("output", help="path to output file, to which the records will be added to the bottom. If the file doesn't exist, it will be created.")
args = parser.parse_args()


#Define variables contained in the secrets.py and configs.py files.
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repositoryID = configs.repositoryID
getDigitalObjectMetadata_list = args.input
getDigitalObjectMetadata_output = args.output

#Authentication
try:
	auth = requests.post(baseURL + '/users/'+user+'/login', params={'password': password}).json()
except requests.exceptions.RequestException as e:
	print("Invalid URL, try again")
	exit()
#Test authentication
if auth.get("session") == None:
	print("Wrong username or password! Try Again")
	exit()
else:
#Print authentication confirmation
	print('Hello ' + auth["user"]["name"] + '. You are logged in.' + '\n')
	
#Set up basic parameters that will be passed through the API, including authentication for each call.
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}


#Open the CSV file and for each line in the CSV . . . 
with open(getDigitalObjectMetadata_list,'r') as csvfile, open(getDigitalObjectMetadata_output,'a', newline='', encoding='utf-8') as csvout:
	csvin = csv.reader(csvfile)
	#next(csvin, None) #ignore header row
	#csvout = json.writer(csvout)
	
	for row in csvin:
	
		#Read the digital object's UID
		digital_object_UID = row[0]
		print ('Processing digital object number ' + digital_object_UID + ' . . .')
		
		#Download the archival object record, into a variable
		digital_object_json = requests.get(baseURL + '/repositories/' + repositoryID + '/digital_objects/' + digital_object_UID , headers=headers).json()
				
		#Print the digital object record to the terminal window (uncomment if you want to use this)
		#print (digital_object_json)
		
		#Write results to output file.
		print ('Adding digital object number ' + digital_object_UID + ' to ' + getDigitalObjectMetadata_output)
		json.dump(digital_object_json, csvout)
		csvout.write('\n')
		
		#New line to terminal, to keep things clean
		print ('\n')
		