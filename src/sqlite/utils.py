from __future__ import annotations

from enum import Enum
from dataclasses import dataclass

@dataclass(slots=True)
class InRecord:
    status: Status
    title: str
    priority: Priority
    due_date: int
    comment: str
    delivered_to: str

@dataclass(slots=True)
class OutRecord(InRecord):
    id: int
    created_at: int
    updated_at: int

class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    URGENT = 3

class Status(Enum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

