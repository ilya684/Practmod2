import sqlite3
from datetime import datetime

from app.models import Note


class StorageError(Exception):
    pass


class SqliteStorage:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = sqlite3.connect(db_file)
        self.connection.row_factory = sqlite3.Row
        self.create_table()
        self.ensure_pinned_column()

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
            raise StorageError(str(error)) from error

    def ensure_pinned_column(self):
        try:
            columns = self.connection.execute(
                "PRAGMA table_info(notes)"
            ).fetchall()

            column_names = [column["name"] for column in columns]

            if "pinned" not in column_names:
                self.connection.execute(
                    "ALTER TABLE notes ADD COLUMN pinned INTEGER NOT NULL DEFAULT 0"
                )
                self.connection.commit()

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

    def get_notes(self, filter_name="all"):
        try:
            if filter_name == "pinned":
                rows = self.connection.execute(
                    """
                    SELECT id, text, created_at, pinned
                    FROM notes
                    WHERE pinned = 1
                    ORDER BY pinned DESC, id DESC
                    """
                ).fetchall()
            elif filter_name == "other":
                rows = self.connection.execute(
                    """
                    SELECT id, text, created_at, pinned
                    FROM notes
                    WHERE pinned = 0
                    ORDER BY id DESC
                    """
                ).fetchall()
            else:
                rows = self.connection.execute(
                    """
                    SELECT id, text, created_at, pinned
                    FROM notes
                    ORDER BY pinned DESC, id DESC
                    """
                ).fetchall()

            return [
                Note(
                    id=row["id"],
                    text=row["text"],
                    created_at=row["created_at"],
                    pinned=bool(row["pinned"]),
                )
                for row in rows
            ]

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

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

            if row is None:
                return None

            return Note(
                id=row["id"],
                text=row["text"],
                created_at=row["created_at"],
                pinned=bool(row["pinned"]),
            )

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

    def create_note(self, text):
        try:
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
            raise StorageError(str(error)) from error

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
            raise StorageError(str(error)) from error

    def delete_note(self, note_id):
        try:
            self.connection.execute(
                "DELETE FROM notes WHERE id = ?",
                (note_id,),
            )
            self.connection.commit()

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

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
            raise StorageError(str(error)) from error

    def delete_all(self):
        try:
            self.connection.execute("DELETE FROM notes")
            self.connection.commit()

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

    def count_notes(self, filter_name="all"):
        try:
            if filter_name == "pinned":
                row = self.connection.execute(
                    "SELECT COUNT(*) AS count FROM notes WHERE pinned = 1"
                ).fetchone()
            elif filter_name == "other":
                row = self.connection.execute(
                    "SELECT COUNT(*) AS count FROM notes WHERE pinned = 0"
                ).fetchone()
            else:
                row = self.connection.execute(
                    "SELECT COUNT(*) AS count FROM notes"
                ).fetchone()

            return row["count"]

        except sqlite3.Error as error:
            raise StorageError(str(error)) from error

    def close(self):
        self.connection.close()
