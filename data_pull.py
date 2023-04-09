from clients.airtable import AirtableClient
from clients.google import GoogleClient
from clients.strava import StravaClient
from clients.weight_gurus import WeightGurusClient
from clients.whoop import WhoopClient

from datetime import date, datetime
from dateutil import tz
from flask import Flask, Response, request
from daily_tracker_row import DailyTrackerRow
from weekly_tracker_row import WeeklyTrackerRow, get_week_name
from pandas import date_range

import os

app = Flask(__name__)

@app.route("/pull", methods=["POST"])
def pull_life_tracker_data():
    
    daily_client    = AirtableClient('daily_tracker')
    strava_client   = StravaClient()
    whoop_client    = WhoopClient()
    weight_client   = WeightGurusClient()
    google_client   = GoogleClient()

    existing_rows = daily_client.get_rows()

    start_date = datetime.fromtimestamp(int(os.environ['THE_BEGINNING_EPOCH']))
    if 'start_date' in request.json:
        start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d')
    elif request.json['full_backfill'] == False:
        sorted_rows = daily_client.get_sorted_rows()
        start_date = datetime.strptime(sorted_rows[-1].date, '%Y-%m-%d')

    today = datetime.now(tz.gettz('America/Los_Angeles'))

    activities = strava_client.get_activities(after=start_date.strftime('%s'))
    sleeps     = whoop_client.get_recent_sleeps(start_date)
    workouts   = whoop_client.get_recent_workouts(start_date)
    cycles     = whoop_client.get_recent_cycles(start_date)
    recoveries = whoop_client.get_recent_recoveries(start_date)
    weights    = weight_client.get_weights(start_date)

    updated_daily_rows = []
    for date_to_process in date_range(start_date.date(), today.date()):
        
        date_str = date_to_process.strftime('%Y-%m-%d')

        # Create row if it's a new date
        if date_str not in existing_rows:
            row = DailyTrackerRow(date=date_to_process)
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
        daily_client.upsert_row(row)
        updated_daily_rows += [row]

    update_weekly_summary(daily_client, updated_daily_rows)

    return Response(
        f'Updated life tracker from {start_date.date()} to today', status=200)

def update_weekly_summary(daily_client, updated_daily_rows):
    weekly_client = AirtableClient('weekly_tracker')
    existing_days = daily_client.get_rows(force_get=True)
    
    weeks_to_update = {}
    for row in updated_daily_rows:
        week_name = get_week_name(row.get_date())
        if week_name in weeks_to_update:
            weeks_to_update[week_name] = weeks_to_update[week_name] + [row]
        else:
            weeks_to_update[week_name] = [row]

    week_names = weeks_to_update.keys()
    weeks_to_days = map_weeks_to_days(week_names, existing_days)
    for week_name in week_names:
        
        # get available day rows for week
        days_for_week = weeks_to_days[week_name]

        # calculate summary
        week_row = WeeklyTrackerRow(day_rows=days_for_week)

        # save row
        weekly_client.upsert_row(week_row)

def map_weeks_to_days(week_names, day_rows):
    
    weeks_to_days = {}
    for day_key, day_row in day_rows.items():
        
        week_name = get_week_name(day_row.get_date())
        if week_name in week_names:

            if week_name in weeks_to_days:                
                weeks_to_days[week_name] += [day_row]
            else:
                weeks_to_days[week_name] = [day_row]

    return weeks_to_days
    