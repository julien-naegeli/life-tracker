import csv
import io
import os
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime
from dateutil import tz

# gwt_header changes when the cronometer app updates. 
# if it no longer works, inspect webapp requests to find the new one
GWT_HEADER = '2D6A926E3729946302DC68073CB0D550' 

class CronometerClient:

    def __init__(self) -> None:

        self.cookies, self.og_cookies = {}, {}
        self.anti_csrf_token = self.get_anti_csrf_token()
        self.session_nonce   = self.login()
        self.user_id         = self.authenticate()
        self.api_nonce       = self.get_api_nonce()

    def _update_cookies(self, new_cookies):
        for cookie in new_cookies:
            self.cookies[cookie.name] = cookie.value

    def get_anti_csrf_token(self):
        
        response = requests.get('https://cronometer.com/login/')
        response_html = BeautifulSoup(response.text, features='html.parser')
        anti_csrf = response_html.body.find('input', attrs={'name': 'anticsrf'})
        
        self._update_cookies(response.cookies)

        return anti_csrf.get('value')

    def login(self):

        url = 'https://cronometer.com/login'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'anticsrf': self.anti_csrf_token,
            'username': os.environ['EMAIL'],
            'password': os.environ['CRONOMETER_PASSWORD']
        }

        response = requests.post(
            url, headers=headers, data=data, cookies=self.cookies)
        
        self._update_cookies(response.cookies)

        return response.cookies['sesnonce']

    def authenticate(self):
        url = 'https://cronometer.com/cronometer/app'
        headers = {
            'content-type': 'text/x-gwt-rpc; charset=UTF-8',
            'x-gwt-module-base': 'https://cronometer.com/cronometer/',
            'x-gwt-permutation': '7B121DC5483BF272B1BC1916DA9FA963'
        }
        data = f'7|0|5|https://cronometer.com/cronometer/|{GWT_HEADER}|' + \
                'com.cronometer.shared.rpc.CronometerService|authenticate|' + \
                'java.lang.Integer/3438268394|1|2|3|4|1|5|5|-300|'

        response = requests.post(
            url, headers=headers, data=data, cookies=self.cookies)

        self.session_nonce = response.cookies['sesnonce']
        self._update_cookies(response.cookies)
        
        return re.search('OK\[(?P<userid>\d*),.*', response.text)[1]

    def get_api_nonce(self):

        url = 'https://cronometer.com/cronometer/app'
        headers = {
            'content-type': 'text/x-gwt-rpc; charset=UTF-8',
            'x-gwt-module-base': 'https://cronometer.com/cronometer/',
            'x-gwt-permutation': '7B121DC5483BF272B1BC1916DA9FA963'
        }
        data = f'7|0|8|https://cronometer.com/cronometer/|{GWT_HEADER}|' + \
                'com.cronometer.shared.rpc.CronometerService|' + \
                'generateAuthorizationToken|java.lang.String/2004016611|I|' + \
                'com.cronometer.shared.user.AuthScope/2065601159|' + \
                f'{self.session_nonce}|1|2|3|4|4|5|6|6|7|8|{self.user_id}|' + \
                '3600|7|2|'

        response = requests.post(
            url, headers=headers, data=data, cookies=self.cookies)

        self._update_cookies(response.cookies)

        return re.search('\"(?P<token>.*)\"', response.text)[1]

    def get_nutrition_summaries(self, start_date, end_date):

        url = 'https://cronometer.com/export'
        params = {
            'generate': 'dailySummary',
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'nonce': self.api_nonce

        }

        response = requests.get(url, params=params, cookies=self.cookies)
        nutrition_summaries = csv.DictReader(io.StringIO(response.text))

        return to_date_dict(nutrition_summaries)

def to_date_dict(nutrition_summaries) -> dict:
    date_dict = {}

    for summary in nutrition_summaries:
        date_dict[summary['Date']] = summary

    return date_dict
