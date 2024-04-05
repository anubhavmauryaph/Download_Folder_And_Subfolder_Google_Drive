from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Define the scopes
from google.colab import auth
from oauth2client.client import GoogleCredentials

# Authentication When You Are In Colab NoteBook
def authenticate():
    auth.authenticate_user()
    credentials = GoogleCredentials.get_application_default()
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service
  
# Authentication When You Are Not In Colab NoteBook

# def authenticate():
#     # Authenticate and create the drive service
#     flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#     credentials = flow.run_console()
#     drive_service = build('drive', 'v3', credentials=credentials)
#     return drive_service


def download_folder(drive_service, folder_id, destination_path):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_path, exist_ok=True)
    # List all files in the folder
    results = drive_service.files().list(q=f"'{folder_id}' in parents and trashed=false", fields="files(id, name, mimeType)").execute()
    items = results.get('files', [])
    for item in items:
        item_name = item['name']
        item_id = item['id']
        item_type = item['mimeType']
        if item_type == 'application/vnd.google-apps.folder':
            # Recursively download subfolders
            download_folder(drive_service, item_id, os.path.join(destination_path, item_name))
        else:
            # Download files
            request = drive_service.files().get_media(fileId=item_id)
            with open(os.path.join(destination_path, item_name), 'wb') as f:
                f.write(request.execute())
            print(f'Downloaded: {item_name}')

if __name__ == '__main__':
    # Replace 'folder_id' with the ID of the shared Google Drive folder
    folder_id = '1XjFMn6-XSAiwQDZAVjvOy8y0poU6cNrR'
    # Replace 'destination_path' with the local directory where you want to save the files
    destination_path = '/content/dd'
    
    drive_service = authenticate()
    download_folder(drive_service, folder_id, destination_path)
