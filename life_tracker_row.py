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

            if 'Sleep Score' in raw_row['fields']:
                self.sleep_score = raw_row['fields']['Sleep Score']
            else:
                self.sleep_score = ''

            if 'Respiratory Rate' in raw_row['fields']:
                self.respiratory_rate = raw_row['fields']['Respiratory Rate']
            else:
                self.respiratory_rate = ''

            if 'Weight' in raw_row['fields']:
                self.weight = raw_row['fields']['Weight']
            else:
                self.weight = ''

            if 'Cals Burned' in raw_row['fields']:
                self.kcals_burned = raw_row['fields']['Cals Burned']
            else:
                self.kcals_burned = None

            if 'Strain' in raw_row['fields']:
                self.strain = raw_row['fields']['Strain']
            else:
                self.strain = None

            if 'AHR' in raw_row['fields']:
                self.avg_heart_rate = raw_row['fields']['AHR']
            else:
                self.avg_heart_rate = None

            if 'MHR' in raw_row['fields']:
                self.max_heart_rate = raw_row['fields']['MHR']
            else:
                self.max_heart_rate = None

            if 'Recovery' in raw_row['fields']:
                self.recovery_score = raw_row['fields']['Recovery']
            else:
                self.recovery_score = None

            if 'RHR' in raw_row['fields']:
                self.rhr = raw_row['fields']['RHR']
            else:
                self.rhr = None

            if 'HRV' in raw_row['fields']:
                self.hrv = raw_row['fields']['HRV']
            else:
                self.hrv = None

            if 'Blood Oxygen' in raw_row['fields']:
                self.blood_oxygen = raw_row['fields']['Blood Oxygen']
            else:
                self.blood_oxygen = None

            if 'Skin Temp' in raw_row['fields']:
                self.skin_temp = raw_row['fields']['Skin Temp']
            else:
                self.skin_temp = None

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
            self.sleep_score = ''
            self.respiratory_rate = ''
            self.weight = ''
            self.kcals_burned = None
            self.strain = None
            self.avg_heart_rate = None
            self.max_heart_rate = None
            self.recovery_score = None
            self.rhr = None
            self.hrv = None
            self.blood_oxygen = None
            self.skin_temp = None
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

        score = sleep_dict[self.date]['score']
        sleep_summary = score['stage_summary']

        time_in_bed = sleep_summary['total_in_bed_time_milli']
        time_awake = sleep_summary['total_awake_time_milli']

        time_asleep = time_in_bed - time_awake

        self.sleep = time_asleep / 1000
        self.sleep_score = score['sleep_performance_percentage']
        self.respiratory_rate = score['respiratory_rate']


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

    def add_whoop_cycles(self, cycle_dict):

        if self.date not in cycle_dict:
            return

        score_summary = cycle_dict[self.date]['score']

        self.strain         = score_summary['strain']
        self.kcals_burned   = score_summary['kilojoule'] / 4.184
        self.avg_heart_rate = score_summary['average_heart_rate']
        self.max_heart_rate = score_summary['max_heart_rate']

    def add_whoop_recoveries(self, recovery_dict):

        if self.date not in recovery_dict:
            return

        score_summary = recovery_dict[self.date]['score']

        self.recovery_score = score_summary['recovery_score']
        self.rhr            = score_summary['resting_heart_rate']
        self.hrv            = score_summary['hrv_rmssd_milli']
        self.blood_oxygen   = score_summary['spo2_percentage']
        self.skin_temp      = score_summary['skin_temp_celsius'] * 1.8 + 32

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

        if self.sleep_score:
            output['Sleep Score'] = self.sleep_score

        if self.respiratory_rate:
            output['Respiratory Rate'] = self.respiratory_rate

        if self.weight:
            output['Weight'] = self.weight

        if self.kcals_burned:
            output['Cals Burned'] = self.kcals_burned

        if self.strain:
            output['Strain'] = self.strain

        if self.avg_heart_rate:
            output['AHR'] = self.avg_heart_rate

        if self.max_heart_rate:
            output['MHR'] = self.max_heart_rate

        if self.recovery_score:
            output['Recovery'] = self.recovery_score

        if self.rhr:
            output['RHR'] = self.rhr

        if self.hrv:
            output['HRV'] = self.hrv

        if self.blood_oxygen:
            output['Blood Oxygen'] = self.blood_oxygen

        if self.skin_temp:
            output['Skin Temp'] = self.skin_temp

        if self.travel_day:
            output['Travel Day'] = self.travel_day

        return output

def get_strava_activity_url(activity):
    return '[' + activity.name + ']' + \
        '(https://www.strava.com/activities/' + str(activity.id) + ')'

