#This script creates new Digital Objects and associates them with existing Archival Object record (one Archival Object per Digital Object). The metadata for the new Digital Object comes from a CSV file, except for the title, which by default comes from the Archival Object. The CSV must specify which Archival Object to associate with each new Digital Object. The resulting Digital Objects are recorded in an output CSV, with their record IDs, metadata, and ID of associated Archival Objects. 

#CSV format: The file's first row must be a header row for column labels, even if that row is empty of any labels. You can use any labels you want (including blank), but the column must contain this content and follow this order, without deviation:
# 1. Archival Object ID
# 2. URL/URI to Digital Object
# 3. Local identifier
# 4. Digital Object Title (Use if you would like to overwrite the assocated Archival Object's title. Otherwise can be left blank)

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

#Open Input CSV and iterate over rows
with open(digital_object_csv,'r') as csvfile, open(updated_digital_object_csv,'a', newline='', encoding='utf-8') as csvout:
	csvin = csv.reader(csvfile)
	next(csvin, None) #ignore header row
	csvout = csv.writer(csvout)
	for row in csvin:
				
		#Make datetime variable formatted as YYYYMMDDHHMMSS
		dt = datetime.datetime.today().strftime('%Y%m%d%H%M%S%f')
		
		#Define metadata: all values for the new DAO record, except title
		archival_object_UID = row[0] 
		new_do_url = row[1]
		new_do_id = dt #FOR TESTING PURPOSES ONLY
		#new_do_id = row[2] #UNCOMMENT FOR PRODUCTION

		#Download the archival object record, into a variable
		archival_object_json = requests.get(baseURL + '/repositories/' + repositoryID + '/archival_objects/' + archival_object_UID ,headers=headers).json()
		
		#Define metadata: title of Digital Object. Script will pull from the CSV file. If the CSV title cell is blank, the Archival Object's title will be used. 
		if not row[3]:
			new_do_title = archival_object_json['display_string']
		else:
			new_do_title = row[3]
		print(new_do_title)

		#Plug the metadata values into a variable that holds the new DAO record (before it's uploaded)
		digital_object_json = {"jsonmodel_type":"digital_object",'title':new_do_title,'digital_object_id':new_do_id,'file_versions':[{'file_uri':new_do_url}]}

		#Format the JSON for the new DAO record
		digital_object_data = json.dumps(digital_object_json)

		#Make the API call to upload the record
		dig_obj_post = requests.post(baseURL + '/repositories/' + repositoryID + '/digital_objects' , headers=headers, data=digital_object_data).json()
		print (dig_obj_post)
		print ('New DO? : ', dig_obj_post['status'])
		
		# Grab the digital object ID
		dig_obj_uri = dig_obj_post['uri']
		dig_obj_id = dig_obj_post['id']

		#Publish the digital object
		dig_obj_publish_all = requests.post(baseURL + dig_obj_uri + '/publish',headers=headers)
				
		# Build a new instance to add to the archival object, which links to the digital object
		dig_obj_instance = {'instance_type':'digital_object', 'digital_object':{'ref':dig_obj_uri}}

		# Append the new instance to the (local copy of the) existing archival object record's instances
		archival_object_json['instances'].append(dig_obj_instance)
		archival_object_data = json.dumps(archival_object_json)
				
		# Repost the archival object
		archival_object_update = requests.post(baseURL + '/repositories/' + repositoryID + '/archival_objects/' + archival_object_UID ,headers=headers,data=archival_object_data).json()
		print ('New DO added as instance of new AO?: ', archival_object_update['status'])

		#Download the new digital object record, into a variable
		digital_object_record = requests.get(baseURL + dig_obj_uri ,headers=headers).json()
		
		#Save the metadata from the downloaded record into local variables
		#archival_object_UID doesn't get pulled back down, because it is only available in the record as the link, not the UID
		uri = digital_object_record['uri']
		digital_object_id = digital_object_record['digital_object_id']
		title = digital_object_record['title']
		restrictions = digital_object_record['restrictions']
		publish = digital_object_record['publish']
		created_by = digital_object_record['created_by']
		repository = digital_object_record['repository']
		system_mtime = digital_object_record['system_mtime']

		#Save the row of metadata variables into a single local variable. 
		new_csv_row = [archival_object_UID,uri,digital_object_id,title,restrictions,publish,created_by,repository,system_mtime]

		#Write this variable to the output csv.
		csvout.writerow(new_csv_row)
		
		#Clear variables
		archival_object_UID = ""
		new_do_url = ""
		new_do_id = ""
		new_do_title = ""
		
		#print a new line for readability in console
		print('\n')