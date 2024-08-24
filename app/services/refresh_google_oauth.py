import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from app.core.config import INITIAL_TOKEN, REFRESH_TOKEN, OAUTH_CLIENT_ID, OAUTH_CLIENT_SECRET


SCOPES = ['https://www.googleapis.com/auth/generative-language.retriever']

def load_creds():
    """Converts `client_secret.json` to a credential object.

    This function caches the generated tokens to minimize the use of the
    consent screen.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('hello.json'):
        creds = Credentials.from_authorized_user_file('hello.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            create_hello_json(token=INITIAL_TOKEN,
                  refresh_token=REFRESH_TOKEN, 
                  token_uri="https://oauth2.googleapis.com/token", 
                  client_id=OAUTH_CLIENT_ID,
                  client_secret=OAUTH_CLIENT_SECRET, 
                  scopes=["https://www.googleapis.com/auth/generative-language.retriever"], 
                  universe_domain="googleapis.com", 
                  account="", expiry="2024-08-24T20:12:44.703164Z")
            creds = Credentials.from_authorized_user_file('hello.json', SCOPES)
        # Save the credentials for the next run
        with open('hello.json', 'w') as token:
            token.write(creds.to_json())
    return creds



def create_hello_json(**kwargs):
    with open('hello.json', 'w') as json_file:
        json.dump(kwargs, json_file)