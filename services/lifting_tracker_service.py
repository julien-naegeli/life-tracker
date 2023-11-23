from clients.airtable import AirtableClient
from datetime import datetime
from models.lifting_tracker_row import LiftingTrackerRow

class LiftingTrackerService:

    def __init__(self, daily_service, start_date):
        self.start_date = start_date
        self.lifting_client = AirtableClient('lifting_tracker')
        self.daily_service = daily_service
        self.lifts = daily_service.get_service_data_with_default('hevy')
        self.existing_rows = self.lifting_client.get_rows()

    def update_rows(self):
        for date, workout in self.lifts.items():
            if datetime.strptime(date, '%Y-%m-%d') >= self.start_date:
                existing_workouts = []
                if date in self.existing_rows:
                    existing_workouts = self.existing_rows[date]

                if len(existing_workouts) > 0:
                    ids = [ew['id'] for ew in existing_workouts]
                    self.lifting_client.batch_delete(ids)

                for exercise in workout['exercises']:
                    new_row = LiftingTrackerRow(date, workout['name'], exercise)
                    self.lifting_client.create_row(new_row)
