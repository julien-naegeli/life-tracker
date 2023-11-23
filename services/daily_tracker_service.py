from clients.cronometer import CronometerClient
from clients.google import GoogleClient
from clients.hevy import HevyClient
from clients.strava import StravaClient
from clients.weight_gurus import WeightGurusClient
from clients.whoop import WhoopClient
from models.daily_tracker_row import DailyTrackerRow
from datetime import datetime
from dateutil import tz
from os import environ
from pandas import date_range


class DailyTrackerService:
    def __init__(self, daily_client, start_date, services):
        self.start_date    = start_date
        self.today         = datetime.now(tz.gettz('America/Los_Angeles'))
        self.date_range    = date_range(start_date.date(), self.today.date())
        self.services      = services
        
        self.daily_client  = daily_client
        self.strava_client = None
        self.whoop_client  = None
        self.google_client = None
        self.weight_client = None
        self.crono_client  = None
        self.hevy_client   = None

        self.strava_activities   = None
        self.whoop_sleeps        = None
        self.whoop_workouts      = None
        self.whoop_cycles        = None
        self.whoop_recoveries    = None
        self.weights             = None
        self.nutrition_summaries = None
        self.lifts               = None

        self.existing_rows = self.daily_client.get_rows()


    def update_rows(self):
        updated_daily_rows = []
        for date_to_process in self.date_range:
            
            date_str = date_to_process.strftime('%Y-%m-%d')

            # Create row if it's a new date
            if date_str not in self.existing_rows:
                row = DailyTrackerRow(date=date_to_process)
            else:
                row = self.existing_rows[date_str]

            for service in self.services:

                # Only executes a fetch if we haven't yet fetched in this run
                data = self.get_service_data_with_default(service)

                # Only updates if there's new data
                self.update_row_if_data_exists(row, service, data)
                
            self.daily_client.upsert_row(row)
            updated_daily_rows += [row]
        
        return updated_daily_rows


    def get_service_data_with_default(self, service, default={}):
        if service in self.services:
            return self.get_service_data(service)
        return default


    def get_service_data(self, service, date=None):
        client = self.get_service_client(service)
        
        if service == 'strava':
            if self.strava_activities == None:    
                after = self.start_date.strftime('%s')
                self.strava_activities = client.get_activities(after=after)
            return self.strava_activities
        elif service == 'whoop.sleep':
            if self.whoop_sleeps == None:
                self.whoop_sleeps = client.get_recent_sleeps(self.start_date)
            return self.whoop_sleeps
        elif service == 'whoop.workout':
            if self.whoop_workouts == None:
                self.whoop_workouts = client.get_recent_workouts(
                    self.start_date)
            return self.whoop_workouts
        elif service == 'whoop.cycle':
            if self.whoop_cycles == None:
                self.whoop_cycles = client.get_recent_cycles(self.start_date)
            return self.whoop_cycles 
        elif service == 'whoop.recovery':
            if self.whoop_recoveries == None:
                self.whoop_recoveries = client.get_recent_recoveries(
                    self.start_date)
            return self.whoop_recoveries
        elif service == 'weight_gurus':
            if self.weights == None:
                self.weights = client.get_weights(self.start_date)
            return self.weights
        elif service == 'google':
            if date == None:
                return []
            return client.get_events(date)
        elif service == 'cronometer':
            if self.nutrition_summaries == None:
                self.nutrition_summaries = client.get_nutrition_summaries(
                    self.start_date, self.today)
            return self.nutrition_summaries
        elif service == 'hevy':
            if self.lifts == None:
                self.lifts = client.get_workouts()
            return self.lifts
        else:
            raise Exception(f'{service} is not a supported service')
        

    def get_service_client(self, service):
        if service == 'strava':
            if not self.strava_client:
                self.strava_client = StravaClient()
            return self.strava_client
        elif 'whoop' in service:
            if not self.whoop_client:
                self.whoop_client = WhoopClient()
            return self.whoop_client
        elif service == 'weight_gurus':
            if not self.weight_client:
                self.weight_client = WeightGurusClient()
            return self.weight_client
        elif service == 'google':
            if not self.google_client:
                self.google_client = GoogleClient()
            return self.google_client
        elif service == 'cronometer':
            if not self.crono_client:
                self.crono_client = CronometerClient()
            return self.crono_client
        elif service == 'hevy':
            if not self.hevy_client:
                self.hevy_client = HevyClient()
            return self.hevy_client
        else:
            raise Exception(f'{service} is not a supported service')


    def update_row_if_data_exists(self, row, service, data):
        if row.date not in data:
            return
        
        if service == 'strava':
            return row.add_strava_activities(data)
        elif service == 'whoop.sleep':
            return row.add_whoop_sleep(data)
        elif service == 'whoop.workout':
            return row.add_whoop_workouts(data)
        elif service == 'whoop.cycle':
            return row.add_whoop_cycles(data)
        elif service == 'whoop.recovery':
            return row.add_whoop_recoveries(data)
        elif service == 'weight_gurus':
            return row.add_weight(data)
        elif service == 'google':
            return row.add_travel_day(data)
        elif service == 'cronometer':
            return row.add_nutrition_summary(data)
        elif service == 'hevy':
            return row.add_hevy_workouts(data)
        else:
            raise Exception(f'{service} is not a supported service')


    def get_start_date(self, params):
        start_date = datetime.fromtimestamp(int(environ['THE_BEGINNING_EPOCH']))
        if 'start_date' in params:
            start_date = datetime.strptime(params['start_date'], '%Y-%m-%d')
        elif params['full_backfill'] == False:
            sorted_rows = self.daily_client.get_sorted_rows()
            start_date = datetime.strptime(sorted_rows[-1].date, '%Y-%m-%d')
        return start_date