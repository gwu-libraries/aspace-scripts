#This script tests whether your authentication credentials in secrets.py are working. It authenticates you, and that's all.

print("Hello. Beginning authentication check . . .\n")
#Import modules and configuration files.
import json
import requests
import secrets #secrets.py is a file that should be in the same directory as this file

#Define variables contained in the secrets.py
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

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
	print("SUCCESS, " + auth["user"]["name"] + "!\nYour secrets.py file successfully logs you into:\n" + " - " + baseURL + "\nwith username:\n - " + user)
	