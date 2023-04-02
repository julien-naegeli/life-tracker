from clients.airtable import AirtableClient
from clients.google import GoogleClient
from clients.strava import StravaClient
from clients.weight_gurus import WeightGurusClient
from clients.whoop import WhoopClient

from datetime import date, datetime
from dateutil import tz
from flask import Flask, Response, request
from life_tracker_row import LifeTrackerRow
from pandas import date_range


import os

app = Flask(__name__)

@app.route("/pull/life-tracker-data", methods=["POST"])
def pull_life_tracker_data():
    
    airtable_client = AirtableClient('life_tracker')
    strava_client   = StravaClient()
    whoop_client    = WhoopClient()
    weight_client   = WeightGurusClient()
    google_client = GoogleClient()

    existing_rows = airtable_client.get_rows()

    start_date = datetime.fromtimestamp(int(os.environ['THE_BEGINNING_EPOCH']))
    if request.json['full_backfill'] == False:
        sorted_rows = airtable_client.get_sorted_rows()
        start_date = datetime.strptime(sorted_rows[-1].date, '%Y-%m-%d')

    today = datetime.now(tz.gettz('America/Los_Angeles'))

    activities = strava_client.get_activities(after=start_date.strftime('%s'))
    sleeps     = whoop_client.get_recent_sleeps(start_date)
    workouts   = whoop_client.get_recent_workouts(start_date)
    cycles     = whoop_client.get_recent_cycles(start_date)
    recoveries = whoop_client.get_recent_recoveries(start_date)
    weights    = weight_client.get_weights(start_date)

    for date_to_process in date_range(start_date.date(), today.date()):
        
        date_str = date_to_process.strftime('%Y-%m-%d')

        # Create row if it's a new date
        if date_str not in existing_rows:
            row = LifeTrackerRow(date=date_to_process)
        else:
            row = existing_rows[date_str]
            
        # Add strava data
        row.add_strava_activities(activities)

        # Add whoop data
        row.add_whoop_sleep(sleeps)
        row.add_whoop_workouts(workouts)
        row.add_whoop_cycles(cycles)
        row.add_whoop_recoveries(recoveries)

        # Add weight gurus data
        row.add_weight(weights)

        # Check if it's a travel day
        events = google_client.get_events(date_to_process)
        row.add_travel_day(events)

        # Save row
        airtable_client.upsert_row(row)

    return Response(
        f'Updated life tracker from {start_date.date()} to today', status=200)
