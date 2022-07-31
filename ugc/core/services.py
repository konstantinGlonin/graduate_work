from __future__ import annotations

import csv
from typing import List, Union

DB: Union[SampleDB, None] = None


def get_db():
    return DB


class SampleDB:
    def __init__(self):
        self.data = {}

    def dump(self):
        return self.data

    def get_keys(self) -> List | None:
        return list(self.data.keys())

    def get(self, key: str) -> List | None:
        if str(key) in self.data:
            return self.data[str(key)]
        return None

    def load_data(self, path: str = 'data/ratings_new.csv'):
        with open(path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['user_id'] in self.data:
                    self.data[row['user_id']].append(row['film_work_id'])
                else:
                    self.data[row['user_id']] = [row['film_work_id']]
