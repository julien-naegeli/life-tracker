from datetime import datetime
from dateutil import tz
from daily_tracker_row import get_pace, format_time

class LiftingTrackerRow:
    
    def __init__(self, date, workout_name, raw_exercise):

        self.date = date
        self.raw_exercise = raw_exercise
        self.workout = workout_name
        self.exercise = raw_exercise['title']

        exercise_stats = self.get_exercise_stats()
        self.working_sets = exercise_stats['working_sets']
        self.working_reps = exercise_stats['working_reps']
        self.weight = exercise_stats['max_weight']
        self.volume = exercise_stats['volume']
        self.personal_records = exercise_stats['personal_records']
        self.muscle_groups = self.get_muscle_groups()

    def get_exercise_stats(self):
        working_sets, working_reps = 0, ''
        max_weight, volume = 0, 0
        reps, weights = [], []
        prs = ''

        for set in self.raw_exercise['sets']:
            if set['indicator'] == 'normal':
                weight = self._get_with_default(set, 'weight_kg', 0) * 2.20462
                working_sets += 1

                if not set['reps']:
                    if set['duration_seconds']:
                        reps += [format_duration(set['duration_seconds'])]
                    elif self.exercise == 'Farmers Walk':
                        reps += [format_duration(set['distance_meters'])]
                    elif set['distance_meters']:
                        reps += [str(set['distance_meters']) + 'm']
                    volume += weight
                else:
                    reps += [set['reps']]
                    weights += [weight]
                    volume += set['reps'] * weight

                if weight > max_weight:
                    max_weight = weight

                if len(set['prs']) > 0:
                    for pr in set['prs']:
                        if len(prs) > 0:
                            prs += ', '
                        else:
                            prs += '🏆 '
                        
                        pr_lbs = str(int(pr['value'] * 2.20462))
                        if pr['type'] == 'best_reps':
                            prs += 'Rep PR: ' + str(int(pr['value']))
                        elif pr['type'] == 'best_weight':
                            prs += 'Weight PR: ' + pr_lbs
                        elif pr['type'] == 'best_volume':
                            prs += 'Volume PR: ' + pr_lbs
                        elif pr['type'] == 'best_1rm':
                            prs += '1RM PR: ' + pr_lbs

        same_reps = all(rep == reps[0] for rep in reps)
        same_weight = all(weight == weights[0] for weight in weights)

        if same_weight and same_reps and len(reps) > 0:
            working_reps = str(reps[0])
        elif same_weight:
            for rep in reps:
                if len(working_reps) > 0:
                    working_reps += ', '
                working_reps += str(rep)
        else:
            for i in range(len(weights)):
                if i > 0:
                    working_reps += ', '
                working_reps += str(reps[i]) + 'x' + str(int(weights[i]))
        
        return {
            'working_sets': working_sets, 
            'working_reps': working_reps, 
            'max_weight': max_weight, 
            'volume': volume,
            'personal_records': prs
        }


    def get_muscle_groups(self):
        muscle_groups = [self._format(self.raw_exercise['muscle_group'])]

        for other_muscle in self.raw_exercise['other_muscles']:
            muscle_groups += [self._format(other_muscle)]

        return muscle_groups
    
    def _format(self, muscle_group):
        if muscle_group == 'full_body':
            return 'Full Body'
        elif muscle_group == 'upper_back':
            return 'Upper Back'
        elif muscle_group == 'lower_back':
            return 'Lower Back'
        else:
            return muscle_group.capitalize()


    def to_dict(self):
       
        output = {
            'Date': self.date,
            'Workout': self.workout,
            'Exercise': self.exercise,
            'Sets': self.working_sets,
            'Reps': self.working_reps,
            'Weight': self.weight,
            'Volume': self.volume,
            'Muscle Groups': self.muscle_groups,
            'PRs': self.personal_records
        }

        return output
    
    def _get_with_default(self, map, key, default=None):
        
        if not map or key not in map:
            return default
        
        if key in ['weight_kg'] and not map[key]:
            return 0

        return map[key]
    
def format_duration(seconds):
    if seconds > 60:
        return str(seconds // 60) + 'm ' + str(seconds % 60) + 's'
    return str(seconds) + 's'