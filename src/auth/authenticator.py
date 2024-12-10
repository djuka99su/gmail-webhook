from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
from config.config import CLIENT_SECRET_PATH, TOKEN_PATH

class GmailAuthenticator:
    SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar',  # Add this line
    'https://www.googleapis.com/auth/calendar.events'  # Add this line
]
    
    @staticmethod
    def authenticate(credentials_path):
        creds = None
        
        if os.path.exists(TOKEN_PATH):
            with open(TOKEN_PATH, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, GmailAuthenticator.SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open(TOKEN_PATH, 'wb') as token:
                pickle.dump(creds, token)

        return creds 
    
