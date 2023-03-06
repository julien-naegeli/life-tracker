from airtable_client import AirtableClient
from datetime import date, datetime
from flask import Flask, Response, request
from life_tracker_row import LifeTrackerRow
from pandas import date_range
from strava_client import StravaClient

import os

app = Flask(__name__)

@app.route("/pull/life-tracker-data", methods=["POST"])
def pull_life_tracker_data():
    
    airtable_client = AirtableClient('life_tracker')
    strava_client   = StravaClient()

    existing_rows = airtable_client.get_rows()

    start_date = datetime.fromtimestamp(int(os.environ['THE_BEGINNING_EPOCH']))
    if request.json['full_backfill'] == False:
        sorted_rows = airtable_client.get_sorted_rows()
        start_date = datetime.strptime(sorted_rows[-1].date, '%Y-%m-%d')

    activities = strava_client.get_activities(after=start_date.strftime('%s'))
    
    if start_date.date() == date.today():
        return Response(
            'No updates. Did you forget to pass in full_backfill?', status=200)

    for date_to_process in date_range(start_date.date(), date.today()):
        
        date_str = date_to_process.strftime('%Y-%m-%d')

        # Create row if it's a new date
        if date_str not in existing_rows:
            row = LifeTrackerRow(date=date_to_process)
        else:
            row = existing_rows[date_str]
            
        # Add strava data
        row.add_strava_activities(activities)

        # Add whoop data


        # Save row
        airtable_client.upsert_row(row)

    return Response(
        f'Updated life tracker from {start_date.date()} to today', status=200)


if __name__ == "__main__":
  app.run()
