from clients.airtable import AirtableClient
from flask import Flask, request
from services.config import SUPPORTED_SERVICES
from services.daily_tracker_service import DailyTrackerService
from services.lifting_tracker_service import LiftingTrackerService
from services.weekly_tracker_service import WeeklyTrackerService
from util.helpers import get_with_default, get_start_date
from util.responses import success


app = Flask(__name__)


@app.route("/pull", methods=["POST"])
def pull_life_tracker_data():
    daily_client = AirtableClient('daily_tracker')

    start_date = get_start_date(request.json)
    services = get_with_default(request.json, 'services', SUPPORTED_SERVICES)
    
    daily_service = DailyTrackerService(daily_client, start_date, services)
    updated_daily_rows = daily_service.update_rows()

    weekly_service = WeeklyTrackerService(daily_client, updated_daily_rows)
    weekly_service.update_summary()

    if 'hevy' in services:
        lifting_service = LiftingTrackerService(daily_service, start_date)
        lifting_service.update_rows()

    return success(f'Updated life tracker from {start_date.date()} to today')


@app.route("/ping", methods=["GET"])
def ping():
    return success('Successful ping. Let\'s track that life.')