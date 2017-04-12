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
    print "wrong argv python backup.py config_file_path upload_file_path"
    sys.exit()

  config_file_path = sys.argv[1]
  upload_file_path = sys.argv[2]

  if os.path.isfile(config_file_path) is False:
    print "not found config file: "+config_file_path
    sys.exit()

  if os.path.isfile(upload_file_path) is False:
    print "not found upload file: " + upload_file_path
    sys.exit()

  mimetype_upload_file = mimetypes.guess_type(upload_file_path)

  #print type(mimetype_upload_file)

  upload_file_mimetype = mimetype_upload_file[0]

  if upload_file_mimetype is None:
    print "could not get mimetype for upload file - using the default"
    upload_file_mimetype = 'application/octet-stream'

  upload_file_title =  os.path.basename(upload_file_path)
  
  with open(config_file_path, 'r') as config_file:
    config = json.loads(config_file.read())
  
  drive_service = helper.createDriveService(config)
  print helper.coloured_output("Authentication is sucessful" , 'green')
  print helper.print_about( drive_service )
  print helper.coloured_output("Uploading file to your google drive" , 'yellow')

  file_result = helper.insert_file( drive_service, config, upload_file_path, upload_file_title,upload_file_mimetype  )
  
  print helper.coloured_output("Uploaded new file done" , 'green')
  #print file_result

  print helper.coloured_output("Getting list of children files" , 'yellow')
  children_files = helper.retrieve_all_files( drive_service, config['backup_folder_id'] )
  # print "children_files", children_files
  #print children_files
  print "This folder have {0} files".format( str(len(children_files)) )

  if len( children_files ) > config['max_file_in_folder']:
    #Remove old backup file
    number_delete_file = len(children_files) - config['max_file_in_folder']
    count = 0
    index_delete_file = len(children_files) -1

    while count < number_delete_file:
      children_id = children_files[index_delete_file]['id']
      print helper.coloured_output( "Removing old file with id " + children_id , 'yellow')
      helper.remove_file( drive_service, children_id )
      count +=1
      index_delete_file -=1

  print helper.coloured_output("Done backup file to google drive !" , 'green')
except Exception, e:
  print "error"
  print e
finally:
  pass

