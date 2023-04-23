from datetime import timedelta
from daily_tracker_row import get_pace, format_time

class WeeklyTrackerRow:
    
    def __init__(self, day_rows):
        
        self.week = get_week_name(day_rows[0].get_date())
        self.day_rows = day_rows
        self.id = None
        self.num_rows = 0
        self.total_sleep_mins = 0
        self.whoop_days = 0
        self.active_days = 0
        self.road_time = 0
        self.road_miles = 0
        self.mountain_time = 0
        self.mountain_miles = 0
        self.elevation_gain = 0
        self.total_strain = 0
        self.total_recovery = 0
        self.weight_days = 0
        self.total_weight = 0
        self.total_cals = 0
        self.total_rhr = 0
        self.total_hrv = 0
        self.total_blood_oxygen = 0
        self.total_skin_temp = 0
        self.total_recovery_score = 0
        self.crono_days = 0
        self.cal_diff = 0
        self.cals_consumed = 0
        self.protein = 0

    def _reset_row(self):
        self.num_rows = 0
        self.total_sleep_mins = 0
        self.active_days = 0
        self.whoop_days = 0
        self.road_time = 0
        self.road_miles = 0
        self.mountain_time = 0
        self.mountain_miles = 0
        self.elevation_gain = 0
        self.total_strain = 0
        self.total_recovery = 0
        self.weight_days = 0
        self.total_weight = 0
        self.total_cals = 0
        self.total_rhr = 0
        self.total_hrv = 0
        self.total_blood_oxygen = 0
        self.total_skin_temp = 0
        self.total_sleep_score = 0
        self.crono_days = 0
        self.cal_diff = 0
        self.cals_consumed = 0
        self.protein = 0

    def summarize_day_rows(self):
        
        self._reset_row()
        
        for day_row in self.day_rows:

            self.road_miles += day_row.road_miles
            self.road_time += day_row.road_time
            self.mountain_miles += day_row.mountain_miles
            self.mountain_time += day_row.mountain_time
            self.elevation_gain += day_row.elevation_gain

            if day_row.exercise.strip() != '':
                self.active_days += 1

            if day_row.sleep:
                self.total_sleep_mins += day_row.sleep
                self.whoop_days += 1

            if day_row.recovery_score:
                self.total_recovery += int(day_row.recovery_score)

            if day_row.strain:
                self.total_strain += day_row.strain

            if day_row.kcals_burned:
                self.total_cals += day_row.kcals_burned

            if day_row.rhr:
                self.total_rhr += day_row.rhr

            if day_row.hrv:
                self.total_hrv += day_row.hrv

            if day_row.blood_oxygen:
                self.total_blood_oxygen += day_row.blood_oxygen
            
            if day_row.skin_temp:
                self.total_skin_temp += day_row.skin_temp
            
            if day_row.sleep_score:
                self.total_sleep_score += day_row.sleep_score

            if day_row.weight:
                self.total_weight += float(day_row.weight)
                self.weight_days  += 1

            if day_row.kcals_consumed:
                self.crono_days += 1
                self.cal_diff += day_row.kcals_consumed - day_row.kcals_burned
                self.cals_consumed += day_row.kcals_consumed
                self.protein += day_row.protein

        self.num_rows = len(self.day_rows)

        return self.to_dict()


    def to_dict(self):
       
        output = {
            
            'Week': self.week,
            'Active Days': self.active_days,

        }

        if self.whoop_days:
            output['Avg. Sleep'] = self.total_sleep_mins / self.whoop_days
            output['Avg. Sleep Score'] = self.total_sleep_score / self.num_rows
            output['Avg. Strain'] = self.total_strain / self.whoop_days
            output['Avg. Recovery'] = self.total_recovery / self.whoop_days
            output['Avg. Cals Burned'] = self.total_cals / self.whoop_days
            output['RHR'] = self.total_rhr / self.whoop_days
            output['HRV'] = self.total_hrv / self.whoop_days
            output['Blood Oxygen'] = self.total_blood_oxygen / self.whoop_days
            output['Skin Temp.'] = self.total_skin_temp / self.whoop_days

        if self.road_miles and self.road_time:
            output['👟 Miles'] = self.road_miles
            output['👟 Pace'] = get_pace(self.road_miles, self.road_time)

        if self.mountain_miles and self.mountain_time:
            output['⛰ Miles'] = self.mountain_miles
            output['⛰ Pace'] = get_pace(self.mountain_miles, self.mountain_time)

        if self.elevation_gain:
            output['Elevation Gain'] = self.elevation_gain

        if self.total_weight:
            output['Avg. Weight'] = f'{self.total_weight / self.weight_days:.1f}'

        if self.cals_consumed:
            output['Avg. Cals Consumed'] = self.cals_consumed / self.crono_days
            output['Cal Diff.'] = get_cal_diff_str(self.cal_diff)
            output['Avg. Protein'] = self.protein / self.crono_days

        return output

def get_week_name(date):
    start_day = date - timedelta(days=date.weekday())
    end_day   = start_day + timedelta(days=6)
    start_str = start_day.strftime('%b %d')
    end_str   = end_day.strftime('%b %d')
    return f'Week {date.isocalendar()[1]}: {start_str} - {end_str}'

def get_cal_diff_str(cal_diff):
    if cal_diff > 0:
        return f'+{int(cal_diff):,}'
    elif cal_diff < 0:
        return f'{int(cal_diff):,}'
    return '0'
