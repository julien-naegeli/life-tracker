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
        self.apiKey = os.environ['AIRTABLE_API_KEY']
        self.table = self.get_table(base_name)
        self.base_name = base_name
        self.rows = None

    def get_table(self, base_name):
        return Table(
            self.apiKey, 
            os.environ[AIRTABLE_CONFIG[base_name]['env_key']], 
            'Main'
        )

    def get_rows(self, as_dict=False, force_get=False):
        if force_get or not self.rows:
            rows = self.table.all()
            if as_dict:
                output = {}
                for row in rows:
                    row_key = AIRTABLE_CONFIG[self.base_name]['row_key']
                    output[row['fields'][row_key]] = self._transform_row(row)
            else:
                output = rows

            self.rows = output
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
        if row_key not in self.get_rows(as_dict=True):
            self.table.create(row)
        else:
            self.table.update(row_id, row)
