from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload
from apiclient import errors
from datetime import datetime
import httplib2, json


def createDriveService(config):
  """Builds and returns a Drive service object authorized with the given config object.
  Returns:
    Drive service object.
  """

  f = file(config['private_key12_path'], 'rb')
  key = f.read()
  f.close()
  # config.service_account Email of the Service Account.
  credentials = SignedJwtAssertionCredentials(config['service_account'], key,
      scope='https://www.googleapis.com/auth/drive')
  http = httplib2.Http()
  http = credentials.authorize(http)

  return build('drive', 'v2', http=http)


def insert_file(service, config, upload_file_path, upload_file_title, upload_file_mimetype ):
  """Insert new file.

  Args:
    service: Drive API service instance.
    config: configuration obj
    description: Description of the file to insert.
    upload_file_title: file title
    upload_file_mimetype: MIME type of the file to upload.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """

  media_body = MediaFileUpload(upload_file_path, mimetype=upload_file_mimetype, resumable=True)
  #Set modifydate is now
  unicode_type = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  #unicode format 2014-08-10T11:33:16.844Z
  body = {
    'title': upload_file_title,
    'description': config['description'],
    'mimeType': upload_file_mimetype,
    'parents': [{'id': config['backup_folder_id']}],
    'modifiedDate': unicode_type
  }
  
  try:
    file = service.files().insert(
      body=body,
      media_body=media_body).execute()

    return file
  except errors.HttpError, error:
    print 'An error occured: %s' % error
    return None


def retrieve_all_files(service, folder_id, trashed=False):
  """Retrieve a list of File resources.

  Args:
    service: Drive API service instance.
  Returns:
    List of File resources.
  """
  result = []
  page_token = None
  while True:
    try:
      #find on folder id and not trashed
      trashed = "false" if trashed == False else "true"
      param = {
        "q": "'%s' in parents and trashed = %s " % (folder_id, trashed)
      }
      
      print "q", param["q"]
      if page_token:
        param['pageToken'] = page_token

      print param

      files = service.files().list(**param).execute()

      result.extend(files['items'])
      page_token = files.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return result


def files_in_folder(service, folder_id, include_download_url = False):
  """Return files belonging to a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to print files from.
  """
  page_token = None
  return_list = []
  while True:
    try:

      param = {}

      if page_token:
        param['pageToken'] = page_token

      children = service.children().list(
          folderId=folder_id, **param).execute()


      for child in children.get('items', ['modifiedDate']):

        if include_download_url:
          file_instance = service.files().get(fileId=child["id"]).execute()
          
          child['download_url'] = file_instance.get('downloadUrl')
          child['title'] = file_instance.get('title')
          child['mimeType'] = file_instance['mimeType']

          #Get revision to get modify date
          revisions = service.revisions().list(fileId=child["id"]).execute()
          first_revision =  revisions.get('items', [])[0]
          #print json.dumps(first_revision)

          child['modifiedDate'] =  first_revision['modifiedDate']
          child['fileSize'] = first_revision['fileSize']

          # revision = service.revisions().get(fileId=file_id, revisionId=revision_id).execute()

          # print 'Revision ID: %s' % revision['id']
          # print 'Modified Date: %s' % revision['modifiedDate']

          #service.revisions().get(fileId=file_id, revisionId=revision_id).execute()

        return_list.append( child )

        
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return return_list

def remove_file(service, file_id):
  """Remove permanently a file from a folder.

  Args:
    service: Drive API service instance.
    file_id: ID of the file to remove from the folder.
  """
  try:
    service.files().delete( fileId=file_id).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error



def print_about(service):
  """Print information about the user along with the Drive API settings.

  Args:
    service: Drive API service instance.
  """
  try:
    about = service.about().get().execute()

    print 'Current user name: %s' % about['name']
    print 'Root folder ID: %s' % about['rootFolderId']
    print 'Total quota (bytes): %s' % about['quotaBytesTotal']
    print 'Used quota (bytes): %s' % about['quotaBytesUsed']
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def coloured_output(out, color):
  mapping_color = {
    'red':31,
    'green':32,
    'yellow':33,
    'blue':34
  }
  if color in mapping_color:
    color = mapping_color[color]

  return '\033[1;%sm--> %s\033[1;m' % (color, out)