from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

# Scope required for YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = None
    # Check if credentials are stored in 'token.pickle'
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If credentials are not valid or available, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            # Use out_of_band flow to get the authorization URL
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            auth_url, _ = flow.authorization_url(prompt='consent')

            print('Please go to this URL and authorize the application:')
            print(auth_url)

            # Get the authorization code from the user
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            creds = flow.credentials

        # Save the credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # Build the YouTube Data API service
    return build('youtube', 'v3', credentials=creds)

def upload_video(video_path, title, description, tags):
    try:
        # Get authenticated YouTube Data API service
        youtube = get_authenticated_service()
        # Proceed only if authentication was successful
        if youtube:
            # Create a request to upload the video
            request = youtube.videos().insert(
                part="snippet,status",
                body={
                  "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22" # Category ID for "People & Blogs"
                  },
                  "status": {
                    "privacyStatus": "public" # Set privacy status to public
                  }
                },
                media_body=video_path # Path to the video file
            )
            # Execute the request and get the response
            response = request.execute()
            print(f"Video uploaded successfully. Video ID: {response['id']}")
        else:
            print("Authentication failed. Unable to upload video.")
    except HttpError as e:
        print(f"An error occurred: {e}")