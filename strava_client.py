from airtable_client import AirtableClient
from external.StravaPythonClient.swagger_client.rest import ApiException

import os
import requests
import external.StravaPythonClient.swagger_client as swagger_client


class StravaClient:
    def __init__(self) -> None:
        access_token = self.authenticate()

        config = swagger_client.Configuration()
        config.access_token = access_token

        apiClient = swagger_client.ApiClient(config)

        self.activity_api = swagger_client.ActivitiesApi(apiClient)
    
    def authenticate(self) -> str:
        airtable_client = AirtableClient('config')
        config = airtable_client.get_rows()

        refresh_token_row = config['STRAVA_REFRESH_TOKEN']
        access_token_row = config['STRAVA_ACCESS_TOKEN']

        oauth_url = get_oauth_url(refresh_token_row['fields']['Value'])
        response = requests.post(oauth_url).json()

        refresh_token_row['fields']['Value'] = response['refresh_token']
        access_token_row['fields']['Value'] = response['access_token']

        airtable_client.upsert_row(refresh_token_row)
        airtable_client.upsert_row(access_token_row)

        return response['access_token']

    def get_activities(self, after: int) -> dict:
        activities = []
        
        try:
            activities = self.activity_api.get_logged_in_athlete_activities(
                after=after)
        except ApiException as e:
            print("Error getting strava activities: %s\n" % e)
    
        return to_start_date_dict(activities)

def to_start_date_dict(activities) -> dict:
    
    start_date_dict = {}
    
    for activity in activities:
    
        start_date = str(activity.start_date_local.date())
    
        if start_date in start_date_dict:
            start_date_dict[start_date] += [activity]
        else:
            start_date_dict[start_date] = [activity]
    
    return start_date_dict

def get_oauth_url(refresh_token):
    return os.environ['STRAVA_TOKEN_ROUTE'] + \
        '?client_id=' + os.environ['STRAVA_CLIENT_ID'] + \
        '&client_secret=' + os.environ['STRAVA_CLIENT_SECRET'] + \
        '&refresh_token=' + refresh_token + \
        '&grant_type=refresh_token'
