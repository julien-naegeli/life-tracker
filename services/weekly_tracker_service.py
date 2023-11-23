from clients.airtable import AirtableClient
from models.weekly_tracker_row import WeeklyTrackerRow, get_week_name

class WeeklyTrackerService:
    
    def __init__(self, daily_client, daily_rows):
        self.daily_rows = daily_rows
        self.daily_client = daily_client
        self.weekly_client = AirtableClient('weekly_tracker')

    def update_summary(self):
        existing_days = self.daily_client.get_rows(force_get=True)
        
        weeks_to_update = {}
        for row in self.daily_rows:
            week_name = get_week_name(row.get_date())
            if week_name in weeks_to_update:
                weeks_to_update[week_name] = weeks_to_update[week_name] + [row]
            else:
                weeks_to_update[week_name] = [row]

        week_names = weeks_to_update.keys()
        weeks_to_days = self.map_weeks_to_days(week_names, existing_days)
        for week_name in week_names:
            
            # get available day rows for week
            days_for_week = weeks_to_days[week_name]

            # calculate summary
            week_row = WeeklyTrackerRow(day_rows=days_for_week)

            # save row
            self.weekly_client.upsert_row(week_row)

    def map_weeks_to_days(self, week_names, day_rows):
        weeks_to_days = {}
        for day_row in day_rows.values():
            
            week_name = get_week_name(day_row.get_date())
            if week_name in week_names:

                if week_name in weeks_to_days:                
                    weeks_to_days[week_name] += [day_row]
                else:
                    weeks_to_days[week_name] = [day_row]

        return weeks_to_days