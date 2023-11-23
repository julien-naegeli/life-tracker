from datetime import datetime, timedelta
from dateutil import tz
from os import environ

def get_with_default(map, key, default=None):
    if key in map:
        return map[key]
    return default

def get_start_date(params):
    if 'full_backfill' in params and params['full_backfill']:
        return get_beginning_date()
    if 'start_date' in params:
        return format_date(params['start_date'])
    if 'services' in params and 'cronometer' in params['services']:
        return today() - timedelta(days=7)
    return today()

def format_date(date):
    return datetime.strptime(date, '%Y-%m-%d')

def get_beginning_date():
    return datetime.fromtimestamp(int(environ['THE_BEGINNING_EPOCH']))

def today():
    return datetime.now(tz.gettz('America/Los_Angeles')).date()