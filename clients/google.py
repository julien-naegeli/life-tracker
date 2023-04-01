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


    def get_events(self, date):

        url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {
            'timeMin': get_utc_datetime_for_date(date), 
            'timeMax': get_midnight_of_date(date), 
            'orderBy': 'startTime', 
            'singleEvents': True
        }
        
        response = requests.get(url, params=params, headers=headers)

        return response.json()['items']

def get_utc_datetime_for_date(date):
    dt = datetime.combine(date, datetime.min.time())
    return dt.astimezone(tz.UTC).replace(tzinfo=None).isoformat() + 'Z'

def get_midnight_of_date(date):
    tomorrow_pt = date + timedelta(days=1)
    tonight_midnight = datetime.combine(tomorrow_pt, datetime.min.time())
    midnight_in_utc = tonight_midnight.astimezone(tz.UTC)
    return midnight_in_utc.replace(tzinfo=None).isoformat() + 'Z'

