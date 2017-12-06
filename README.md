# ArchivesSpace (ASpace) Scripts
Scripts using ArchivesSpace's API for querying, adding to, and updating ArchivesSpace data. 

Please note that these scripts have not been fully tested and aren't guaranteed to be working as described below. Please test first before using.

##To prepare scripts for use:

Make a copy of secrets.py and configs.py from /templates_EDIT_THESE, and put it in the same folder as the other .py scripts. 
Open the /configs/secrets.py file and enter all variables.
Open the /configs/configs.py file and enter all necessary variables. Different variables are required for different scripts, so you may not need to fill in all variables.


## getDigitalObjectMetadata.py
This script wants you to give it a text file that lists existing Digital Objects' IDs in ArchivesSpace, and in return it will write you a file with the metadata of those Digital Objects.

##makeDigitalObject.py
This script wants you to give it a CSV file with metadata for new Digital Objects, and in return it will create those Digital Objects, link them to existing Archival Objects, and then confirm the metadata of the newly-created files to a CSV file.

##updateDigitalObjectMetadata.py
This script wants you to give it a CSV file with mew metadata for existing Digital Objects, and in return it will update that metadata, and then confirm the metadata of the newly-created files to a CSV file.

##Authentication.py
This script tests to make sure that your authentication info in the secrets.py file can get you logged into your ArchivesSpace instance. 


Tested with:
- ArchivesSpace 1.4.2
- Python 3.5.1