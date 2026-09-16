import logging
import sqlite3
from datetime import datetime

from app.models import Note


logger = logging.getLogger(__name__)


class StorageError(Exception):
    pass


class SqliteStorage:
    def __init__(self, db_file):
        try:
            self.connection = sqlite3.connect(db_file)
            self.connection.row_factory = sqlite3.Row
            self.create_table()
        except sqlite3.Error as error:
            logger.exception("Database initialization failed")
            raise StorageError(
                "Unable to initialize database"
            ) from error

    def create_table(self):
        try:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    pinned INTEGER NOT NULL DEFAULT 0
                )
                """
            )
            self.connection.commit()
        except sqlite3.Error as error:
            logger.exception("Database table creation failed")
            raise StorageError(
                "Unable to create notes table"
            ) from error

    def get_notes(self, filter_name="all"):
        query = """
            SELECT id, text, created_at, pinned
            FROM notes
        """

        if filter_name == "pinned":
            query += " WHERE pinned = 1"
        elif filter_name == "other":
            query += " WHERE pinned = 0"

        query += " ORDER BY id DESC"

        try:
            rows = self.connection.execute(query).fetchall()
        except sqlite3.Error as error:
            logger.exception("Failed to load notes")
            raise StorageError(
                "Unable to load notes"
            ) from error

        return [
            Note(
                id=row["id"],
                text=row["text"],
                created_at=row["created_at"],
                pinned=bool(row["pinned"]),
            )
            for row in rows
        ]

    def get_note(self, note_id):
        try:
            row = self.connection.execute(
                """
                SELECT id, text, created_at, pinned
                FROM notes
                WHERE id = ?
                """,
                (note_id,),
            ).fetchone()
        except sqlite3.Error as error:
            logger.exception("Failed to load note")
            raise StorageError(
                "Unable to load note"
            ) from error

        if row is None:
            return None

        return Note(
            id=row["id"],
            text=row["text"],
            created_at=row["created_at"],
            pinned=bool(row["pinned"]),
        )

    def create_note(self, text):
        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        try:
            cursor = self.connection.execute(
                """
                INSERT INTO notes (text, created_at, pinned)
                VALUES (?, ?, 0)
                """,
                (text, created_at),
            )
            self.connection.commit()
            return cursor.lastrowid
        except sqlite3.Error as error:
            self.connection.rollback()
            logger.exception("Failed to create note")
            raise StorageError(
                "Unable to create note"
            ) from error

    def update_note(self, note_id, text):
        try:
            self.connection.execute(
                """
                UPDATE notes
                SET text = ?
                WHERE id = ?
                """,
                (text, note_id),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            logger.exception("Failed to update note")
            raise StorageError(
                "Unable to update note"
            ) from error

    def delete_note(self, note_id):
        try:
            self.connection.execute(
                """
                DELETE FROM notes
                WHERE id = ?
                """,
                (note_id,),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            logger.exception("Failed to delete note")
            raise StorageError(
                "Unable to delete note"
            ) from error

    def delete_all(self):
        try:
            self.connection.execute("DELETE FROM notes")
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            logger.exception("Failed to delete all notes")
            raise StorageError(
                "Unable to delete notes"
            ) from error

    def toggle_pin(self, note_id):
        try:
            self.connection.execute(
                """
                UPDATE notes
                SET pinned = CASE pinned
                    WHEN 1 THEN 0
                    ELSE 1
                END
                WHERE id = ?
                """,
                (note_id,),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            self.connection.rollback()
            logger.exception("Failed to change pin state")
            raise StorageError(
                "Unable to change pin state"
            ) from error

    def count_notes(self, filter_name="all"):
        if filter_name == "pinned":
            query = (
                "SELECT COUNT(*) FROM notes "
                "WHERE pinned = 1"
            )
        elif filter_name == "other":
            query = (
                "SELECT COUNT(*) FROM notes "
                "WHERE pinned = 0"
            )
        else:
            query = "SELECT COUNT(*) FROM notes"

        try:
            return self.connection.execute(
                query
            ).fetchone()[0]
        except sqlite3.Error as error:
            logger.exception("Failed to count notes")
            raise StorageError(
                "Unable to count notes"
            ) from error

    def close(self):
        try:
            self.connection.close()
        except sqlite3.Error as error:
            logger.exception("Failed to close database")
            raise StorageError(
                "Unable to close database"
            ) from error
