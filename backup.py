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

import helper
import json
import mimetypes
import os
import ntpath


try:
  if __name__ != '__main__':
    print "not allow"
    sys.exit()


  current_file = os.path.realpath(__file__)
  current_path = os.path.dirname(current_file)
  print current_path
  os.chdir(current_path)

  print sys.argv
  if len(sys.argv) != 3:
    print "wrong argv python backup.py config_file_path upload_file_path"
    sys.exit()

  config_file_path = sys.argv[1]
  upload_file_path = sys.argv[2]

  if  os.path.isfile(config_file_path) is False:
    print "not found config file: "+config_file_path
    sys.exit()

  if  os.path.isfile(upload_file_path) is False:
    print "not found upload file: " + upload_file_path
    sys.exit()

  mimetype_upload_file = mimetypes.guess_type(upload_file_path)

  #print type(mimetype_upload_file)

  upload_file_mimetype = mimetype_upload_file[0]

  if mimetype_upload_file is None:
    print "could not get mimetype for upload file"
    sys.exit()

  upload_file_title =  os.path.basename(upload_file_path)
  
  
  config_file = open(config_file_path, 'r')
  config = json.loads(config_file.read())

  
  drive_service = helper.createDriveService(config)
  print "Authentication is sucessful"

  file_result = helper.insert_file( drive_service, config, upload_file_path, upload_file_title,upload_file_mimetype  )
  print "Uploaded new file done"
  #print file_result

  print "Getting list of children files"
  children_files = helper.files_in_folder( drive_service, config['backup_folder_id'] )
  #print children_files
  print len( "This folder have " + str(len(children_files)) )

  if len( children_files ) > config['max_file_in_folder']:
    #Remove old backup file
    number_delete_file = len(children_files) - config['max_file_in_folder']
    count = 0
    index_delete_file = len(children_files) -1

    while count < number_delete_file:
      children_id = children_files[index_delete_file]['id']
      print "Removing file with id " + children_id
      helper.remove_file_from_folder( drive_service, config['backup_folder_id'], children_id )
      count +=1
      index_delete_file -=1

  print "Done backup file to google drive !"
except Exception, e:
  print "error"
  print e
finally:
  pass

