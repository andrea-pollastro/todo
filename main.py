from __future__ import annotations

from src.sqlite.db import Database
from src.sqlite.utils import InRecord, Status, Priority
from src.log.utils import set_logger
import logging
import time

set_logger(level=logging.INFO)

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
    for i in range(5):
        db.insert_task(record)
    records = db.get_all_tasks()
    # for r in records:
    #     print(r)
    db.close_connection()
