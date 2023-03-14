from airtable_client import AirtableClient
from datetime import datetime
from dateutil import tz

import os
import requests

class WhoopClient:
    def __init__(self) -> None:
        self.access_token = self.authenticate()

    def authenticate(self) -> str:
        airtable_client = AirtableClient('config')
        config = airtable_client.get_rows()

        refresh_token_row = config['WHOOP_REFRESH_TOKEN']
        access_token_row = config['WHOOP_ACCESS_TOKEN']

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token_row['fields']['Value'],
            'client_id': os.environ['WHOOP_CLIENT_ID'],
            'client_secret': os.environ['WHOOP_CLIENT_SECRET'],
            'scope': 'offline',
        }
        
        url = os.environ['WHOOP_TOKEN_ROUTE']
        response = requests.post(url, data=data).json()
        
        refresh_token_row['fields']['Value'] = response['refresh_token']
        access_token_row['fields']['Value'] = response['access_token']

        airtable_client.upsert_row(refresh_token_row)
        airtable_client.upsert_row(access_token_row)

        return response['access_token']


    def get_recent_sleeps(self, from_date):
        
        url = 'https://api.prod.whoop.com/developer/v1/activity/sleep'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {'start': from_date.strftime('%Y-%m-%dT%H:%M:%SZ')}

        response = requests.get(url, params=params, headers=headers)
        
        return to_date_dict(response.json()['records'])

    def get_recent_workouts(self, from_date):
        
        url = 'https://api.prod.whoop.com/developer/v1/activity/workout'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {'start': from_date.strftime('%Y-%m-%dT%H:%M:%SZ')}

        response = requests.get(url, params=params, headers=headers)
        
        return to_workout_dict(response.json()['records'])


def to_date_dict(sleeps) -> dict:
    date_dict = {}

    for sleep in sleeps:
        sleep_dt = datetime.strptime(sleep['end'].split('T')[0], '%Y-%m-%d')
        date_dict[str(sleep_dt.date())] = sleep

    return date_dict

def to_workout_dict(workouts) -> dict:
    date_dict = {}
    
    for workout in workouts:

        raw_start = datetime.strptime(workout['start'], '%Y-%m-%dT%H:%M:%S.%fZ')
        start_utc = raw_start.replace(tzinfo=tz.tzutc())
        start_pt = start_utc.astimezone(tz.gettz('America/Los_Angeles'))

        start_date = datetime.strftime(start_pt, '%Y-%m-%d')
        if start_date in date_dict:
            date_dict[start_date] += [workout]
        else:
            date_dict[start_date] = [workout]

    return date_dict