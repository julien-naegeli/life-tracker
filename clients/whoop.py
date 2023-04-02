from clients.airtable import AirtableClient
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

    def get_recent_cycles(self, from_date):
        
        url = 'https://api.prod.whoop.com/developer/v1/cycle'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {'start': from_date.strftime('%Y-%m-%dT%H:%M:%SZ')}

        response = requests.get(url, params=params, headers=headers)
        
        return to_cycle_dict(response.json()['records'])

    def get_recent_recoveries(self, from_date):
        
        url = 'https://api.prod.whoop.com/developer/v1/recovery'
        headers = {'Authorization': 'Bearer ' + self.access_token}
        params = {'start': from_date.strftime('%Y-%m-%dT%H:%M:%SZ')}

        response = requests.get(url, params=params, headers=headers)

        return to_recovery_dict(response.json()['records'])


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

def to_cycle_dict(cycles) -> dict:
    date_dict = {}

    for cycle in cycles:
        cycle_dt = datetime.strptime(cycle['start'].split('T')[0], '%Y-%m-%d')
        date_dict[str(cycle_dt.date())] = cycle

    return date_dict

def to_recovery_dict(recoveries) -> dict:
    date_dict = {}

    for recovery in recoveries:
        dt = datetime.strptime(recovery['created_at'].split('T')[0], '%Y-%m-%d')
        date_dict[str(dt.date())] = recovery

    return date_dict