from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, List
import sqlite3
import logging

from .utils import InRecord, DBRecord, Priority, Status

logger = logging.getLogger(__name__)

class Database:

    def __init__(self, db_name: str, dev: bool):
        self.db_name, self.db_path = self._resolve_db_path(db_name, dev)
        try:
            connection = sqlite3.connect(self.db_path)
        except Exception:
            logger.critical("Failed to establish database connection (name=%s, path=%s)", db_name, self.db_path, exc_info=True)
            raise
        
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA journal_mode = WAL;")
        connection.execute("PRAGMA synchronous = NORMAL;")
        connection.execute("PRAGMA foreign_keys = ON;")
        connection.execute("PRAGMA busy_timeout = 5000;")

        self._connection = connection
        logger.info('Database connection established (name=%s, dir=%s)', self.db_name, self.db_path)
        logger.debug("SQLite pragmas set: WAL, synchronous=NORMAL, foreign_keys=ON, busy_timeout=5000ms")
        
    def close_connection(self) -> None:
        self._connection.close()
        logger.info("Database connection closed (name=%s)", self.db_name)

    def create_database(self) -> None:
        logger.debug("Creating database schema if not exists...")
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS organizations(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            );

            CREATE TABLE IF NOT EXISTS tasks(
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
        logger.info("Database schema ready")
    
    def insert_task(self, record: InRecord) -> Optional[int]:
        delivered_to_id: Optional[int] = None

        if record.delivered_to and record.delivered_to.strip():
            delivered_to_id = self._insert_organization(record.delivered_to)
        
        with self._connection:
            cur = self._connection.execute(
                """
                INSERT INTO tasks(status, title, priority, due_date, comment, delivered_to)
                VALUES(?, ?, ?, ?, ?, ?)
                RETURNING *
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
            row = cur.fetchone()
        logger.info("Inserted task '%s' (id=%d, delivered_to(FK)=%s, created_at=%d, updated_at=%d)",
                    record.title, row['id'], delivered_to_id, row['created_at'], row['updated_at'])
        return cur.lastrowid
    
    def get_all_tasks(self) -> List[DBRecord]:
        logger.debug("Retrieving all tasks")
        rows = self._connection.execute("SELECT * FROM tasks").fetchall()
        logger.info("Retrieved %d tasks", len(rows))
        return [DBRecord(**dict(r)) for r in rows]

    def update(self):
        raise NotImplementedError('Not implemented yet')
    
    def delete(self):
        raise NotImplementedError('Not implemented yet')

    # ==================== HELPERS ==================== #
    def _insert_organization(self, name: str) -> int:
        name_norm = self._normalize_organization_name(name)
        logger.debug("Ensuring organization exists: raw='%s', normalized='%s'", name, name_norm)

        organization_id = self._retrieve_organization_id(name_norm)
        if organization_id is not None:
            logger.debug("Organization exists: '%s' (id=%s)", name_norm, organization_id)
            return organization_id
        
        with self._connection:
            self._connection.execute(
                "INSERT OR IGNORE INTO organizations(name) VALUES(?)", (name_norm, )
            )
        # logger.info("Inserting new organization '%s'", name_norm)
        org_id = self._retrieve_organization_id(name_norm)
        if org_id is None:
            logger.error("Failed to create or retrieve organization: '%s'", name_norm)
            raise RuntimeError("Failed to create or retrieve organization id.")
        logger.info("Inserted new organization '%s' (id=%s)", name_norm, org_id)
        return org_id

    def _normalize_organization_name(self, name: str) -> str:
        return " ".join(map(str.capitalize, name.split()))

    def _retrieve_organization_id(self, name: str) -> Optional[int]:
        row = self._connection.execute(
            """
            SELECT id
            FROM organizations
            WHERE name = ?
            """, (name,)
        ).fetchone()
        organization_id = row['id'] if row else None
        logger.debug("Lookup organization '%s' -> id=%s", name, organization_id)
        return organization_id

    def _resolve_db_path(self, db_name: str, dev: bool) -> Tuple[Optional[str], Path]:
        if dev:
            logger.info("Using in-memory database (development mode)")
            return None, Path(":memory:")

        if not db_name or not db_name.strip():
            logger.error("Invalid db_name provided: %s", db_name)
            raise ValueError("Please insert a valid db_name.")

        if not db_name.endswith(".db"):
            db_name = f"{db_name}.db"

        db_path = Path("database") / db_name
        db_path.parent.mkdir(parents=True, exist_ok=True)

        logger.debug("Resolved database path: %s", db_path)
        return db_name, db_path
