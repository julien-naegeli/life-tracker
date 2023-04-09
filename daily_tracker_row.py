from datetime import datetime
from math import modf

class DailyTrackerRow:
    def __init__(self, raw_row={}, date=None):

        self.raw_row = raw_row

        if self.raw_row:
            self.id = raw_row['id']
            self.date = raw_row['fields']['Date']
        else:
            self.id = None
            self.date = date.strftime('%Y-%m-%d')

        self.day_of_week = self._get_with_default('Day')
        self.exercise = self._get_with_default('Exercise', '')
        self.sleep = self._get_with_default('Sleep')
        self.sleep_score = self._get_with_default('Sleep Score')
        self.respiratory_rate = self._get_with_default('Respiratory Rate')
        self.weight = self._get_with_default('Weight')
        self.kcals_burned = self._get_with_default('Cals Burned')
        self.strain = self._get_with_default('Strain')
        self.avg_heart_rate = self._get_with_default('AHR')
        self.max_heart_rate = self._get_with_default('MHR')
        self.recovery_score = self._get_with_default('Recovery')
        self.rhr = self._get_with_default('RHR')
        self.hrv = self._get_with_default('HRV')
        self.blood_oxygen = self._get_with_default('Blood Oxygen')
        self.skin_temp = self._get_with_default('Skin Temp')
        self.travel_day = self._get_with_default('Travel Day', False)
        self.road_miles = self._get_with_default('👟 Miles', 0)
        self.road_time = self._get_with_default('👟 Time', 0)
        self.mountain_miles = self._get_with_default('⛰ Miles', 0)
        self.mountain_time = self._get_with_default('⛰ Time', 0)
        self.elevation_gain = self._get_with_default('Elevation Gain', 0)
        self.strava_link = self._get_with_default('Strava Link')

    def __str__(self):
        return str(self.raw_row)

    def _get_with_default(self, key, default=None):
        
        if not self.raw_row or 'fields' not in self.raw_row:
            return default

        if key in self.raw_row['fields']:
            return self.raw_row['fields'][key]
        
        return default

    def get_date(self):
        return datetime.strptime(self.date, '%Y-%m-%d').date()

    def has_strava(self) -> bool:
        return self.strava_link != ''

    def add_strava_activities(self, activity_dict):

        if self.date not in activity_dict:
            return

        for activity in activity_dict[self.date]:
            
            self.strava_link = get_strava_activity_url(activity)
            sport_type = activity.sport_type

            if sport_type == 'Run':
                
                if '👟' not in self.exercise:
                    self.exercise += '👟 '

                if not self.road_miles:
                    self.road_miles += activity.distance / 1609.344
                if not self.road_time:
                    self.road_time += activity.moving_time
                if not self.elevation_gain:
                    self.elevation_gain += activity.total_elevation_gain * 3.28084

            elif sport_type in ['Hike', 'TrailRun']:
                
                if sport_type == 'Hike' and '🥾' not in self.exercise:
                    self.exercise += '🥾 '
                
                if sport_type == 'TrailRun' and '⛰' not in self.exercise:
                    self.exercise += '⛰ '
                
                if not self.mountain_miles:
                    self.mountain_miles += activity.distance / 1609.344
                if not self.mountain_time:
                    self.mountain_time += activity.moving_time
                if not self.elevation_gain:
                    self.elevation_gain += activity.total_elevation_gain * 3.28084

            elif sport_type == 'Ride' and '🚲' not in self.exercise:
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
            elif workout['sport_id'] == 0 and '👟' not in self.exercise and \
                '⛰' not in self.exercise:
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
            output['Recovery'] = str(int(self.recovery_score))

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

        if self.strava_link:
            output['Strava Link'] = self.strava_link

        if self.road_miles:
            output['👟 Miles'] = self.road_miles

        if self.road_time:
            output['👟 Time'] = self.road_time

        if self.road_miles and self.road_time:
            output['👟 Pace'] = get_pace(self.road_miles, self.road_time)

        if self.mountain_miles:
            output['⛰ Miles'] = self.mountain_miles

        if self.mountain_time:
            output['⛰ Time'] = self.mountain_time

        if self.mountain_miles and self.mountain_time:
            output['⛰ Pace'] = get_pace(self.mountain_miles, self.mountain_time)

        if self.elevation_gain:
            output['Elevation Gain'] = self.elevation_gain

        return output

def get_strava_activity_url(activity):
    return '[' + activity.name + ']' + \
        '(https://www.strava.com/activities/' + str(activity.id) + ')'

def get_pace(miles, time):
    return time / miles * 60

def format_time(time):
    sec_ratio, mins = math.modf(pace)
    return f'{int(mins)}:{int(sec_ratio*60)}'

