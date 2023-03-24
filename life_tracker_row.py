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

            if 'Sleep' in raw_row['fields']:
                self.sleep = raw_row['fields']['Sleep']
            else:
                self.sleep = ''

            if 'Weight' in raw_row['fields']:
                self.weight = raw_row['fields']['Weight']
            else:
                self.weight = ''

            if 'Travel Day' in raw_row['fields']:
                self.travel_day = raw_row['fields']['Travel Day']
            else:
                self.travel_day = False

            if 'Strava Link' in raw_row['fields']:
                self.strava_link = raw_row['fields']['Strava Link']
            else:
                self.strava_link = ''

        elif date:
            self.id = None
            self.exercise = ''
            self.sleep = ''
            self.weight = ''
            self.travel_day = False
            self.strava_link = None
            self.date = date.strftime('%Y-%m-%d')

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
                self.exercise += '👟 '
            elif activity.sport_type == 'Hike' and '🥾' not in self.exercise:
                self.exercise += '🥾 '
            elif activity.sport_type == 'TrailRun' and '⛰' not in self.exercise:
                self.exercise += '⛰ '
            elif activity.sport_type == 'Ride' and '🚲' not in self.exercise:
                self.exercise += '🚲 '
            else:
                continue

    def add_whoop_sleep(self, sleep_dict):
        
        if self.date not in sleep_dict:
            return

        sleep_summary = sleep_dict[self.date]['score']['stage_summary']

        time_in_bed = sleep_summary['total_in_bed_time_milli']
        time_awake = sleep_summary['total_awake_time_milli']

        time_asleep = time_in_bed - time_awake

        self.sleep = time_asleep / 1000


    def add_whoop_workouts(self, workout_dict):
        
        if self.date not in workout_dict:
            return

        for workout in workout_dict[self.date]:
            
            if workout['sport_id'] == 45 and '💪' not in self.exercise:
                self.exercise = '💪 ' + self.exercise
            elif workout['sport_id'] == 0 and '👟' not in self.exercise:
                self.exercise += '👟 '
            elif workout['sport_id'] == 52 and '🥾' not in self.exercise:
                self.exercise += '🥾 '
            elif workout['sport_id'] == 1 and '🚲' not in self.exercise:
                self.exercise += '🚲 '
            elif workout['sport_id'] == 34 and '🎾' not in self.exercise:
                self.exercise += '🎾 '
            elif workout['sport_id'] == 30 and '⚽️' not in self.exercise:
                self.exercise += '⚽️ '
            elif workout['sport_id'] == 44 and '🧘‍♂️' not in self.exercise:
                self.exercise += '🧘‍♂️ '
            elif workout['sport_id'] == 101 and '🥒' not in self.exercise:
                self.exercise += '🥒 '
            else:
                continue

    def add_weight(self, weight_dict):

        if self.date not in weight_dict:
            return

        weight_str = str(weight_dict[self.date]['weight'])
        
        self.weight = f'{weight_str[:3]}.{weight_str[3:]}'


    def add_travel_day(self, events):
        for event in events:
            if '✈️' in event['summary']:
                self.travel_day = True
                return


    def to_dict(self):
       
        output = {'Date': self.date}
        
        if self.strava_link:
            output['Strava Link'] = self.strava_link

        if self.exercise:
            output['Exercise'] = self.exercise.strip()

        if self.sleep:
            output['Sleep'] = self.sleep

        if self.weight:
            output['Weight'] = self.weight

        if self.travel_day:
            output['Travel Day'] = self.travel_day

        return output

def get_strava_activity_url(activity):
    return '[' + activity.name + ']' + \
        '(https://www.strava.com/activities/' + str(activity.id) + ')'

