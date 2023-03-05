class LifeTrackerRow:
    def __init__(self, raw_row=None, date=None):
        if raw_row:

            self.raw_row = raw_row
            
            self.id = raw_row['id']
            self.date = raw_row['fields']['Date']
            self.day_of_week = raw_row['fields']['Day']

            if 'Exercise' in raw_row['fields']:
                self.exercise = raw_row['fields']['Exercise']
            else:
                self.exercise = ''

            if 'Strava Link' in raw_row['fields']:
                self.strava_link = raw_row['fields']['Strava Link']
            else:
                self.strava_link = ''

        elif date:
            self.id = None
            self.strava_link = None
            self.exercise = ''
            self.date = str(date)

    def __str__(self):
        return str(self.raw_row)

    def has_strava(self) -> bool:
        return self.strava_link != ''

    def add_strava_activities(self, activity_dict):

        if self.date not in activity_dict:
            return

        for activity in activity_dict[self.date]:
            
            self.strava_link = get_strava_activity_url(activity)
            
            if activity.sport_type == 'Run' and '👟' not in self.exercise:
                self.exercise += '👟'
            elif activity.sport_type == 'Hike' and '🥾' not in self.exercise:
                self.exercise += '🥾'
            elif activity.sport_type == 'TrailRun' and '⛰' not in self.exercise:
                self.exercise += '⛰'
            elif activity.sport_type == 'Ride' and '🚲' not in self.exercise:
                self.exercise += '🚲'
            else:
                continue

    def to_dict(self):
       
        output = {'Date': self.date}
        
        if self.strava_link:
            output['Strava Link'] = self.strava_link

        if self.exercise:
            output['Exercise'] = self.exercise                        

        return output

def get_strava_activity_url(activity):
    return '[' + activity.name + ']' + \
        '(https://www.strava.com/activities/' + str(activity.id) + ')'

