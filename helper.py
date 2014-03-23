from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from apiclient.http import MediaFileUpload
from apiclient import errors

import httplib2


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
  body = {
    'title': upload_file_title,
    'description': config['description'],
    'mimeType': upload_file_mimetype,
    'parents': [{'id': config['backup_folder_id']}]
  }
  
  try:
    file = service.files().insert(
      body=body,
      media_body=media_body).execute()

    return file
  except errors.HttpError, error:
    print 'An error occured: %s' % error
    return None


def files_in_folder(service, folder_id):
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
        return_list.append( child )
        
      page_token = children.get('nextPageToken')
      if not page_token:
        break
    except errors.HttpError, error:
      print 'An error occurred: %s' % error
      break
  return return_list

def remove_file_from_folder(service, folder_id, file_id):
  """Remove a file from a folder.

  Args:
    service: Drive API service instance.
    folder_id: ID of the folder to remove the file from.
    file_id: ID of the file to remove from the folder.
  """
  try:
    service.children().delete(folderId=folder_id, childId=file_id).execute()
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

