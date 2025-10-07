from __future__ import annotations

from pathlib import Path
from dataclasses import dataclass
from enum import Enum
import sqlite3

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3

class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2


@dataclass
class Record:
    status: Status
    title: str
    priority: Priority
    due_date: int
    comment: str
    delivered_to: str

class Database:

    def __init__(self, dev: bool = False):
        database = ':memory:' if dev else Path('database') / 'todo.db'
        if database != ':memory:':
            database.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(database)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode = WAL;")
        self.connection.execute("PRAGMA synchronous = NORMAL;")
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.connection.execute("PRAGMA busy_timeout = 5000;")

    def create_database(self):
        self.connection.executescript(
        """
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE tasks(
            id              INTEGER PRIMARY KEY,
            status          INTEGER NOT NULL 
                                CHECK (status IN (0, 1, 2))
                                DEFAULT 0,
            title           TEXT NOT NULL,
            priority        INTEGER NOT NULL 
                                CHECK (priority IN (0, 1, 2, 3))
                                DEFAULT 1,
            due_date        INTEGER,
            comment         TEXT,
            delivered_to    INTEGER,
            created_at      INTEGER NOT NULL DEFAULT(unixepoch()),
            updated_at      INTEGER NOT NULL DEFAULT(unixepoch()),
            FOREIGN KEY(delivered_to) REFERENCES organizations(id)
                ON DELETE SET NULL
                ON UPDATE CASCADE
        );

        CREATE TRIGGER IF NOT EXISTS tasks_updated_at
        AFTER UPDATE OF status, title, priority, due_date, comment
            ON tasks
        FOR EACH ROW
        BEGIN
            UPDATE tasks 
            SET updated_at = unixepoch()
            WHERE OLD.id = id;
        END;

        """)

    def create(self):
        with self.connection:
            ...
    
    def read(self):
        ...
    
    def update(self):
        ...
    
    def delete(self):
        ...

