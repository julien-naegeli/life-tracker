from datetime import datetime
from dateutil import tz

import os
import json
import requests

class HevyClient:
    def __init__(self) -> None:
        self.headers = {
            'x-api-key': 'with_great_power',
            'Content-Type': 'application/json',
            'accept-encoding':'gzip'
        }
        self.username = os.environ['HEVY_USERNAME']
        self.password = os.environ['HEVY_PASSWORD']

        self.access_token = self.authenticate()
        self.headers['auth-token'] = self.access_token

    
    def authenticate(self) -> str:
        data = json.dumps({
            'emailOrUsername': self.username,
            'password': self.password
        })

        url = 'https://api.hevyapp.com/login'
        response = requests.post(url, data=data, headers=self.headers).json()
        
        return response['auth_token']
    
    def get_workouts(self):
        params = {
            'username': 'jnaegz',
            'limit': 10,
            'offset': 0
        }
        url = 'https://api.hevyapp.com/user_workouts_paged'

        workouts = []
        num_new_workouts = 10
        while num_new_workouts == 10:
            
            r = requests.get(url, params=params, headers=self.headers).json()
            
            num_new_workouts = len(r['workouts'])
            workouts = workouts + r['workouts']

            params['offset'] += 10

        return to_date_dict(workouts)

    
def to_date_dict(workouts) -> dict:
    date_dict = {}

    for workout in workouts:
        raw_start_date = datetime.utcfromtimestamp(workout['start_time'])
        start_date_utc = raw_start_date.replace(tzinfo=tz.tzutc())
        start_date = start_date_utc.astimezone(tz.gettz('America/Los_Angeles'))
        start_date_formatted = start_date.strftime("%Y-%m-%d")
        date_dict[start_date_formatted] = workout

    return date_dict