#Automatic backup your file to Google Drive

Althought I could make the backup file on my server but I don't trust it, sometime my server could be crash or harddisk get problem.

So this tool help you auto backup your file to google drive by using Google Drive API and this's good service to make sure my file is safe, I think.

it's use if you want make sure your data is backuped daily such as sql data, database, upload folder ,etc.

###Note

if you want backup a folder, you must compress it first, also, you can compress file to faster backup time.

###Preparing:

1. Install goolge api package for python

		easy_install --upgrade google-api-python-client

   or

		pip install --upgrade google-api-python-client

2. you  create your google drive api first at [Link](https://code.google.com/apis/console/b/0/).

3. You create service account to access this , after create service account, you download the private key to somewhere such as I put at path "configs/74214843aee8aba9f11b7825e0a22ef1f06533b7-privatekey.p12" and copy service account id such as "xxxxx-5kfab22qfu82uub2887gi0c9e6eincmu@developer.gserviceaccount.com"
4. You come back to your google drive [drive.google.com](https://drive.google.com) and create share folder( you create an empty folder and right click on the folder and share to user xxxxx-5kfab22qfu82uub2887gi0c9e6eincmu@developer.gserviceaccount.com  ) and copy the folder id ( You can look at the url after visit folder and the id is there ) and in my case the backup folder url is https://drive.google.com/#folders/0B0XTTQmH9aXreFdxS0txVU5Xb1U so that the id is 0B0XTTQmH9aXreFdxS0txVU5Xb1U

5.  Create config file( such as config_file.json ) and input into this file with json format such as

		{
			"service_account":"xxxxx-5kfab22qfu82uub2887gi0c9e6eincmu@developer.gserviceaccount.com",
			"private_key12_path":"configs/74214843aee8aba9f11b7825e0a22ef1f06533b7-privatekey.p12",
			"backup_folder_id":"0B0XTTQmH9aXreFdxS0txVU5Xb1U",
			"description" : "Description for backup file",
			"max_file_in_folder": 5
		}

You can see "max_file_in_folder" that is the number max file on backup folder, so if I backup new file to that folder and that's sixth file. so the oldest file will be removed, this solution to prevent google drive is out of capacity.



###using :

    python backup.py path/configs/config_file.json /path/backup_file.tar.gz

*To automatic backup, you can put this script in crontab and decide the schedule for it.*
##Done