
#Import modules and configuration files.
import json
import requests
import secrets #secrets.py is a file that should be in the same directory as this file
import configs #configs.py is a file that should be in the same directory as this file
import datetime
import csv


#Define variables contained in the secrets.py and configs.py files.
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repositoryID = configs.repositoryID
digital_object_csv = configs.digital_object_csv
updated_digital_object_csv  = configs.updated_digital_object_csv 

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
	print("Hello " + auth["user"]["name"] + ". You are logged in.")
	
#Set up basic parameters that will be passed through the API, including authentication for each call.
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

#Query operator for archival object ID
digital_object_UID = input('What is the digital object ID?')
print (digital_object_UID)

#Download the archival object record, into a variable
digital_object_json = requests.get(baseURL + '/repositories/' + repositoryID + '/digital_objects/' + digital_object_UID , headers=headers).json()
		
#Print the digital object record, into a variable 
print (digital_object_json)