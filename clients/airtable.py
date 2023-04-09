from daily_tracker_row import DailyTrackerRow
from pyairtable import Table

import os

AIRTABLE_CONFIG = {
    'daily_tracker': {
        'env_key': 'LIFE_TRACKER_BASE_ID',
        'row_key': 'Date',
        'table_name': 'Main',
        'has_row_object': True
    },
    'weekly_tracker': {
        'env_key': 'LIFE_TRACKER_BASE_ID',
        'row_key': 'Week',
        'table_name': 'Weekly',
        'has_row_object': False
    },
    'config': {
        'env_key': 'CONFIG_BASE_ID',
        'row_key': 'Key',
        'table_name': 'Main',
        'has_row_object': False
    }
}

class AirtableClient:
    def __init__(self, base_name) -> None:
        self.api_key = os.environ['AIRTABLE_API_KEY']
        self.row_key = AIRTABLE_CONFIG[base_name]['row_key']
        self.env_key = AIRTABLE_CONFIG[base_name]['env_key']

        self.table_name = AIRTABLE_CONFIG[base_name]['table_name']
        self.table = self.get_table(base_name)
        self.base_name = base_name
        
        self.rows = None
        self.rows_dict = None

    def get_table(self, base_name):
        return Table(self.api_key, os.environ[self.env_key], self.table_name)

    def get_rows(self, force_get=False):
        if force_get or self.rows_dict == None:
            rows = self.table.all()
            output = {}
            for row in rows:
                output[row['fields'][self.row_key]] = self._transform_row(row)
            self.rows_dict = output
        return self.rows_dict

    def get_sorted_rows(self, force_get=False):
        if force_get or self.rows == None:
            rows = self.table.all()
            rows = sorted(rows, key=lambda row: row['fields'][self.row_key])
            self.rows = [self._transform_row(row) for row in rows]
        return self.rows

    def _transform_row(self, row):
        if self.base_name == 'daily_tracker':
            return DailyTrackerRow(raw_row=row)
        else:
            return row

    def _get_row_id(self, row):
        row_key = row[AIRTABLE_CONFIG[self.base_name]['row_key']]
        if AIRTABLE_CONFIG[self.base_name]['has_row_object']:
            return self.get_rows()[row_key].id
        else:
            return self.get_rows()[row_key]['id']

    def upsert_row(self, row):
        if self.base_name == 'daily_tracker':
            row = row.to_dict()
        elif self.base_name == 'weekly_tracker':
            row = row.summarize_day_rows()
        else:
            row = row['fields']

        row_key = row[AIRTABLE_CONFIG[self.base_name]['row_key']]
        if row_key in self.get_rows():
            self.table.update(self._get_row_id(row), row)
        else:
            self.table.create(row)
