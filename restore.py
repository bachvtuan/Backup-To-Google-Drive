"""
  @reference links
  http://stackoverflow.com/questions/12211859/i-cant-see-the-files-and-folders-created-via-code-in-my-google-drive/12218662#12218662
  http://stackoverflow.com/questions/13736394/which-google-apis-can-be-accessed-with-service-account-authorization
  https://developers.google.com/drive/web/service-accounts
  https://appengine.google.com/permissions?&app_id=s~sixth-trainer-527
  https://developers.google.com/drive/web/service-accounts
  https://developers.google.com/drive/v2/reference/permissions/insert#try-it
  https://developers.google.com/quickstart/
  https://developers.google.com/drive/v2/reference/files/insert
  https://developers.google.com/drive/v2/reference/children/list
  https://developers.google.com/drive/web/search-parameters
"""

import sys
import json
from datetime import datetime
import mimetypes
import os
import ntpath

import helper

try:
  if __name__ != '__main__':
    print "not allow"
    sys.exit()

  current_file = os.path.realpath(__file__)
  current_path = os.path.dirname(current_file)

  os.chdir(current_path)

  print sys.argv

  if len(sys.argv) != 3:
    print helper.coloured_output("wrong argv python restore.py config_file_path restore_path" , 'red')
    print helper.coloured_output("Example: python restore.py configs/abc.com.json /var/www/" , 'blue')
    sys.exit()

  config_file_path = sys.argv[1]
  restore_path = sys.argv[2]

  if  os.path.isfile(config_file_path) is False:
    print "not found config file: "+config_file_path
    sys.exit()

  if os.path.exists(current_path) is False:
    print "not found restore path: "+config_file_path
    print "make sure this's a folder"
    sys.exit()
  
  config_file = open(config_file_path, 'r')
  config = json.loads(config_file.read())

  drive_service = helper.createDriveService(config)
  print helper.coloured_output("Authentication is sucessful" , 'green')

  print helper.coloured_output("Getting list of children files" , 'yellow')

  children_files = helper.files_in_folder( drive_service, config['backup_folder_id'], True )

  if len( children_files ) == 0:
    print helper.coloured_output("Not found any file on your backup folder to restoring" , 'red')
    sys.exit()

  # if len( children_files ) > 0:
  #   print json.dumps(children_files)


  print "I found {} files on your backup folder, the more small number is newer file version: ".format( len(children_files) )
  index = 1
  for children in children_files:
    
    #Convert unicode to datetime object
    modify_date = datetime.strptime(children['modifiedDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
    print "version {} on {}".format( str(index), modify_date.strftime('%Y-%m-%d %H:%M:%S %Z') )
    index +=1

  print "What's file do you want to download[ Input number, 1 is newsest, [1, {}] ]".format( str( len(children_files) ) )
  file_index = raw_input("Your answer: ")

  if file_index is None or file_index.isdigit() is False:
    file_index = "1"

#  print "file_index is "  + file_index

  file_index = int(file_index) - 1

  #Choose newsest file if user input wrong 
  file_index = 0 if file_index < 0 or file_index >= len( children_files ) else file_index


  select_file = children_files[ file_index ]

  download_url = select_file["download_url"]

  file_path = os.path.join(restore_path, "{}.{}".format( str(file_index + 1), select_file["title"])) 

  print helper.coloured_output("Restoring to " + file_path, 'yellow')  

  if download_url:
    resp, content = drive_service._http.request(download_url)
    if resp.status == 200:
      #print 'Status: %s' % resp
      #print json.dumps(resp)

      handle = file( file_path,'wb')
      handle.write(content)
      handle.close()
      print helper.coloured_output("Restored to " + file_path, 'green')  
      #return content
    else:
      print helper.coloured_output('An error occurred: %s' % resp, 'red')  
      #return None


except Exception, e:
  print 
  print helper.coloured_output("error when restoring", 'red')
  print e
finally:
  pass

