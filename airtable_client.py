from life_tracker_row import LifeTrackerRow
from pyairtable import Table

import os

AIRTABLE_CONFIG = {
    'life_tracker': {
        'env_key': 'LIFE_TRACKER_BASE_ID',
        'row_key': 'Date'
    },
    'config': {
        'env_key': 'CONFIG_BASE_ID',
        'row_key': 'Key'
    }
}

class AirtableClient:
    def __init__(self, base_name) -> None:
        self.api_key = os.environ['AIRTABLE_API_KEY']
        self.row_key = AIRTABLE_CONFIG[base_name]['row_key']
        self.env_key = AIRTABLE_CONFIG[base_name]['env_key']

        self.table = self.get_table(base_name)
        self.base_name = base_name
        
        self.rows = None
        self.rows_dict = None

    def get_table(self, base_name):
        return Table(self.api_key, os.environ[self.env_key], 'Main')

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
        if self.base_name == 'life_tracker':
            return LifeTrackerRow(raw_row=row)
        else:
            return row

    def upsert_row(self, row):
        if self.base_name == 'life_tracker':
            row_id = row.id
            row = row.to_dict()
        else:
            row_id = row['id']
            row = row['fields']

        row_key = row[AIRTABLE_CONFIG[self.base_name]['row_key']]
        if row_key not in self.get_rows():
            self.table.create(row)
        else:
            self.table.update(row_id, row)
