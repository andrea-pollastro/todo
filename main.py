from __future__ import annotations

from src.sqlite.db import Database
from src.sqlite.utils import InRecord, Status, Priority
from pprint import pprint
import logging
import time

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    db = Database(dev=True, db_name='test')
    db.create_database()

    record = InRecord(
        status=Status.IN_PROGRESS,
        title='My first task',
        priority=Priority.HIGH,
        due_date=int(time.time()),
        comment='',
        delivered_to=' piergiorgio  andrei  '
    )
    db.insert(record)
    records = db.retrieve_db()
    db.close_connection()
