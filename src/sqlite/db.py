from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple
import sqlite3
import logging

from utils import InRecord, OutRecord

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:

    def __init__(self, db_name: str, dev: bool):
        self.db_name, self.db_path = self._resolve_db_path(db_name, dev)
        connection = sqlite3.connect(self.db_path)

        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = WAL;")
        connection.execute("PRAGMA synchronous = NORMAL;")
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute("PRAGMA busy_timeout = 5000;")

        self._connection = connection
        logger.info('Connection established with %s in %s', self.db_name, self.db_path)
        
    def close(self):
        self._connection.close()

    def create_database(self):
        self._connection.executescript(
            """
            CREATE TABLE organizations(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
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
            """
        )
    
    def create(self, record: InRecord):
        delivered_to_id: Optional[int] = None

        if record.delivered_to and record.delivered_to.strip():
            delivered_to_id = self._insert_organization(record.delivered_to)
        
        with self._connection:
            self._connection.execute(
                """
                INSERT INTO tasks(status, title, priority, due_date, comment, delivered_to)
                VALUES(?, ?, ?, ?, ?, ?)
                """,
                (
                    record.status.value,
                    record.title,
                    record.priority.value,
                    record.due_date,
                    record.comment,
                    delivered_to_id
                )
            )
    
    def retrieve_db(self):
        cursor = self._connection.cursor()
        res = cursor.execute("SELECT * FROM tasks")
        return res.fetchall()

    def update(self):
        raise NotImplementedError('Not implemented yet')
    
    def delete(self):
        raise NotImplementedError('Not implemented yet')

    def _insert_organization(self, name: str) -> int:
        name_norm = self._normalize_organization_name(name)
        organization_id = self._retrieve_organization_id(name_norm)
        if organization_id is not None:
            return organization_id
        
        with self._connection:
            self._connection.execute(
                "INSERT OR IGNORE INTO organizations(name) VALUES(?)", (name_norm, )
            )
        org_id = self._retrieve_organization_id(name_norm)
        if org_id is None:
            raise RuntimeError("Failed to create or retrieve organization id.")
        
        return org_id

    def _normalize_organization_name(self, name: str) -> str:
        return ' '.join(map(str.capitalize, name.split()))

    def _retrieve_organization_id(self, name: str) -> Optional[int]:
        cursor = self._connection.cursor()
        res = cursor.execute(
            """
            SELECT id
            FROM organizations
            WHERE name = ?
            """, (name,)
        )
        row = res.fetchone()
        organization_id = row['id'] if row else None
        return organization_id

    def _resolve_db_path(self, db_name: str, dev: bool) -> Tuple[Optional[str], str]:
        if dev:
            return None, ":memory:"

        if not db_name or not db_name.strip():
            raise ValueError("Please insert a valid db_name.")

        if not db_name.endswith(".db"):
            db_name = f"{db_name}.db"

        db_path = Path("database") / db_name
        db_path.parent.mkdir(parents=True, exist_ok=True)

        return db_name, str(db_path)
