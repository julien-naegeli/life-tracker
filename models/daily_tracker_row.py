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

        # whoop
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
        
        # google
        self.travel_day = self._get_with_default('Travel Day', False)
        
        # strava
        self.road_miles = self._get_with_default('👟 Miles', 0)
        self.road_time = self._get_with_default('👟 Time', 0)
        self.mountain_miles = self._get_with_default('⛰ Miles', 0)
        self.mountain_time = self._get_with_default('⛰ Time', 0)
        self.elevation_gain = self._get_with_default('Elevation Gain', 0)
        self.workout_link = self._get_with_default('Workout Link', '')

        # cronometer
        self.kcals_consumed = self._get_with_default('Cals Consumed', 0)
        self.protein = self._get_with_default('Protein (g)', 0)
        self.fat = self._get_with_default('Fat (g)', 0)
        self.carbs = self._get_with_default('Carbs (g)', 0)
        self.vitamin_a = self._get_with_default('Vitamin A (μg)', 0)
        self.vitamin_c = self._get_with_default('Vitamin C (mg)', 0)
        self.vitamin_d = self._get_with_default('Vitamin D (IU)', 0)
        self.vitamin_e = self._get_with_default('Vitamin E (mg)', 0)
        self.vitamin_k = self._get_with_default('Vitamin K (μg)', 0)
        self.calcium = self._get_with_default('Calcium (mg)', 0)
        self.copper = self._get_with_default('Copper (mg)', 0)
        self.iron = self._get_with_default('Iron (mg)', 0)
        self.magnesium = self._get_with_default('Magnesium (mg)', 0)
        self.potassium = self._get_with_default('Potassium (mg)', 0)
        self.selenium = self._get_with_default('Selenium (µg)', 0)
        self.sodium = self._get_with_default('Sodium (mg)', 0)
        self.zinc = self._get_with_default('Zinc (mg)', 0)
        self.fiber = self._get_with_default('Fiber (g)', 0)
        self.starch = self._get_with_default('Starch (g)', 0)
        self.sugars = self._get_with_default('Sugars (g)', 0)
        self.net_carbs = self._get_with_default('Net Carbs (g)', 0)
        self.cholesterol = self._get_with_default('Cholesterol (mg)', 0)
        self.monounsaturated = self._get_with_default('Monounsaturated (g)', 0)
        self.polyunsaturated = self._get_with_default('Polyunsaturated (g)', 0)
        self.saturated_fats = self._get_with_default('Saturated (g)', 0)
        self.trans_fats = self._get_with_default('Trans-Fats (g)', 0)
        self.omega_3 = self._get_with_default('Omega-3 (g)', 0)
        self.omega_6 = self._get_with_default('Omega-6 (g)', 0)

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

    def add_strava_activities(self, activity_dict):

        if self.date not in activity_dict:
            return

        for activity in activity_dict[self.date]:
            
            strava_link = get_strava_activity_url(activity)
            if strava_link not in self.workout_link:
                if len(self.workout_link) > 0:
                    self.workout_link = strava_link + ', ' + self.workout_link
                else:
                    self.workout_link = strava_link

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
        if score == None or 'stage_summary' not in score:
            return
        
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
            elif workout['sport_id'] == 52 and '🥾' not in self.exercise and \
                '⛰' not in self.exercise:
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
        if score_summary['skin_temp_celsius']:
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

    def add_nutrition_summary(self, nutrition_summary_dict):
        
        if self.date not in nutrition_summary_dict:
            return

        nutrition_summary = nutrition_summary_dict[self.date]

        self.kcals_consumed = to_float(nutrition_summary['Energy (kcal)'])
        self.protein = to_float(nutrition_summary['Protein (g)'])
        self.fat = to_float(nutrition_summary['Fat (g)'])
        self.carbs = to_float(nutrition_summary['Carbs (g)'])
        self.vitamin_a = to_float(nutrition_summary['Vitamin A (Âµg)'])
        self.vitamin_c = to_float(nutrition_summary['Vitamin C (mg)'])
        self.vitamin_d = to_float(nutrition_summary['Vitamin D (IU)'])
        self.vitamin_e = to_float(nutrition_summary['Vitamin E (mg)'])
        self.vitamin_k = to_float(nutrition_summary['Vitamin K (Âµg)'])
        self.calcium = to_float(nutrition_summary['Calcium (mg)'])
        self.copper = to_float(nutrition_summary['Copper (mg)'])
        self.iron = to_float(nutrition_summary['Iron (mg)'])
        self.magnesium = to_float(nutrition_summary['Magnesium (mg)'])
        self.potassium = to_float(nutrition_summary['Potassium (mg)'])
        self.selenium = to_float(nutrition_summary['Selenium (Âµg)'])
        self.sodium = to_float(nutrition_summary['Sodium (mg)'])
        self.zinc = to_float(nutrition_summary['Zinc (mg)'])
        self.fiber = to_float(nutrition_summary['Fiber (g)'])
        self.starch = to_float(nutrition_summary['Starch (g)'])
        self.sugars = to_float(nutrition_summary['Sugars (g)'])
        self.net_carbs = to_float(nutrition_summary['Net Carbs (g)'])
        self.cholesterol = to_float(nutrition_summary['Cholesterol (mg)'])
        self.monounsaturated = to_float(nutrition_summary['Monounsaturated (g)'])
        self.polyunsaturated = to_float(nutrition_summary['Polyunsaturated (g)'])
        self.saturated_fats = to_float(nutrition_summary['Saturated (g)'])
        self.trans_fats = to_float(nutrition_summary['Trans-Fats (g)'])
        self.omega_3 = to_float(nutrition_summary['Omega-3 (g)'])
        self.omega_6 = to_float(nutrition_summary['Omega-6 (g)'])

    def add_hevy_workouts(self, workout_dict):

        if self.date not in workout_dict:
            return
        
        workout = workout_dict[self.date]

        if '💪' not in self.exercise:
            self.exercise = '💪 ' + self.exercise

        hevy_url = get_hevy_workout_url(workout)

        if hevy_url not in self.workout_link:
            if len(self.workout_link) > 0:
                if self.workout_link[-1] == '\n':
                    self.workout_link = self.workout_link[:-1]
                self.workout_link += ', '
            self.workout_link += hevy_url

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

        if self.workout_link:
            output['Workout Link'] = self.workout_link

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

        if self.kcals_consumed:
            output['Cals Consumed'] = self.kcals_consumed
            output['Protein (g)'] = self.protein
            output['Fat (g)'] = self.fat
            output['Carbs (g)'] = self.carbs
            output['Vitamin A (μg)'] = self.vitamin_a
            output['Vitamin C (mg)'] = self.vitamin_c
            output['Vitamin D (IU)'] = self.vitamin_d
            output['Vitamin E (mg)'] = self.vitamin_e
            output['Vitamin K (μg)'] = self.vitamin_k
            output['Calcium (mg)'] = self.calcium
            output['Copper (mg)'] = self.copper
            output['Iron (mg)'] = self.iron
            output['Magnesium (mg)'] = self.magnesium
            output['Potassium (mg)'] = self.potassium
            output['Selenium (µg)'] = self.selenium
            output['Sodium (mg)'] = self.sodium
            output['Zinc (mg)'] = self.zinc
            output['Fiber (g)'] = self.fiber
            output['Starch (g)'] = self.starch
            output['Sugars (g)'] = self.sugars
            output['Net Carbs (g)'] = self.net_carbs
            output['Cholesterol (mg)'] = self.cholesterol
            output['Monounsaturated (g)'] = self.monounsaturated
            output['Polyunsaturated (g)'] = self.polyunsaturated
            output['Saturated (g)'] = self.saturated_fats
            output['Trans-Fats (g)'] = self.trans_fats
            output['Omega-3 (g)'] = self.omega_3
            output['Omega-6 (g)'] = self.omega_6

        return output

def get_strava_activity_url(activity):
    return '[' + activity.name + ']' + \
        '(https://www.strava.com/activities/' + str(activity.id) + ')'

def get_pace(miles, time):
    return time / miles * 60

def format_time(time):
    sec_ratio, mins = math.modf(pace)
    return f'{int(mins)}:{int(sec_ratio*60)}'

def to_float(s):
    try:
        f = float(s)
    except ValueError:
        f = 0.0
    return f

def get_hevy_workout_url(workout):
    return '[' + workout['name'] + ']' + \
        '(https://hevy.com/workout/' + str(workout['short_id']) + ')'