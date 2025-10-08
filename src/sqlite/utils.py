from __future__ import annotations

from enum import Enum
from dataclasses import dataclass
import sqlite3

@dataclass(slots=True)
class InRecord:
    status: Status
    title: str
    priority: Priority
    due_date: int
    comment: str
    delivered_to: str

@dataclass(slots=True)
class DBRecord(InRecord):
    id: int
    created_at: int
    updated_at: int

    def __post_init__(self):
        if not isinstance(self.status, Status):
            self.status = Status(self.status)
        if not isinstance(self.priority, Priority):
            self.priority = Priority(self.priority)

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3

class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

