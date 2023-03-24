import os.path
import flask
import requests

from clients.airtable import AirtableClient
from datetime import datetime, timedelta
from dateutil import tz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleClient:
    def __init__(self):
        self.authenticate()

    def authenticate(self):

        airtable_client = AirtableClient('config')
        config = airtable_client.get_rows()

        refresh_token_row = config['GOOGLE_REFRESH_TOKEN']
        access_token_row = config['GOOGLE_ACCESS_TOKEN']

        url  = os.environ['GOOGLE_TOKEN_ROUTE']
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token_row['fields']['Value'],
            'client_id': os.environ['GOOGLE_CLIENT_ID'],
            'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
        }

        response = requests.post(url, data=data).json()

        self.access_token = response['access_token']


    def get_events(self):

        today_pt = datetime.now(tz.gettz('America/Los_Angeles'))
        tomorrow_pt = today_pt + timedelta(days=1)
        tonight_midnight = datetime.combine(tomorrow_pt, datetime.min.time())
        midnight_in_utc = tonight_midnight.astimezone(tz.UTC)
        midnight = midnight_in_utc.replace(tzinfo=None).isoformat() + 'Z'

        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {
            'timeMin': now, 
            'timeMax': midnight, 
            'orderBy': 'startTime', 
            'singleEvents': True
        }
        
        response = requests.get(url, params=params, headers=headers).json()

        return response['items']