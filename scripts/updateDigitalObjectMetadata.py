#This script edits existing Digital Objects with a CSV of new metadata.

#Import modules and configuration files.
import json
import requests
import secrets
import configs
import datetime
import csv

#Define variables contained in the secrets.py and configs.py files.
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password
repositoryID = configs.repositoryID 
digital_object_csv_input = "digital_object_csv_input.csv"

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
	print('\n')
	
#Set up basic parameters that will be passed through the API, including authentication for each call.
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

#Ask operator to identify the input and output CSV files.
print ("Enter full filepath of input CSV.")
print ("This file should have digital object id in first row.")
digital_object_csv = input()
print ("")

#Open Input CSV and iterate over rows
with open(digital_object_csv,'r') as csvfile, open(digital_object_csv_input,'a', newline='', encoding='utf-8') as csvout:
	csvin = csv.reader(csvfile)
	next(csvin, None) 
	csvout = csv.writer(csvout)
	for row in csvin:
				
		#Make datetime variable formatted as YYYYMMDDHHMMSS
		dt = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')
		
		#Define input DO UID
		if not row[0]:
			print("Missing the UID for this digital object!")
		else:
			do_UID = row[0] #Existing digital object ID from URL
		
		# Use input DO UID to submit a get request for the digital object and store the JSON
		digital_object_json = requests.get(baseURL + '/repositories/' + repositoryID + '/digital_objects/' + do_UID , headers=headers).json()

		#Save the metadata from the downloaded record into local variables
		#archival_object_UID 
		uri = digital_object_json['uri']
		digital_object_id = digital_object_json['digital_object_id']
		title = digital_object_json['title']
		restrictions = digital_object_json['restrictions']
		publish = digital_object_json['publish']
		created_by = digital_object_json['created_by']
		repository = digital_object_json['repository']
		system_mtime = digital_object_json['system_mtime']
		print (uri)
		
		#Save the row of metadata variables into a single local variable. 
		new_csv_row = [uri,digital_object_id,title,restrictions,publish,created_by,repository,system_mtime]
		print (new_csv_row)

		#Write this variable to the output csv.
		csvout.writerow(new_csv_row)


		print('\n')