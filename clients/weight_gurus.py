from cmath import nan
from datetime import datetime
from dateutil import tz
import json
import os

import requests

class WeightGurusClient:

    def __init__(self):
    
        self.access_token = self._login()

    def _login(self):

        url = 'https://api.weightgurus.com/v3/account/login'
        data = {
            'email': os.environ['EMAIL'],
            'password': os.environ['WEIGHT_GURUS_PASSWORD'],
            'web': True
        }
    
        response = requests.post(url, data=data).json()
        
        return response['accessToken']


    def get_weights(self, start_date=None):
        
        if not start_date:
            start_date = 'start=2023-01-01T01:00:00.000Z'

        url = f'https://api.weightgurus.com/v3/operation/?start={start_date}'
        headers = {'authorization': f"Bearer {self.access_token}"}

        response = requests.get(url, headers=headers)

        return to_weight_dict(response.json()['operations'])

def to_weight_dict(weights) -> dict:
    date_dict = {}
    
    for weight in weights:

        start_time = convert_to_pt(weight['entryTimestamp'])
        start_date = datetime.strftime(start_time, '%Y-%m-%d')
        
        if start_date in date_dict:
            old_time = convert_to_pt(date_dict[start_date]['entryTimestamp'])
            if start_time < old_time:
                continue
                
        date_dict[start_date] = weight


    return date_dict

def convert_to_pt(time):
        raw_start = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')
        start_utc = raw_start.replace(tzinfo=tz.tzutc())
        return start_utc.astimezone(tz.gettz('America/Los_Angeles'))





