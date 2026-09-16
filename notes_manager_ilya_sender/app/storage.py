import sqlite3

from app.models import Note


class SqliteStorage:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.connection.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
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

    def get_notes(self, filter_name="all"):
        query = """
            SELECT id, text, created_at, pinned
            FROM notes
        """
        params = []

        if filter_name == "pinned":
            query += " WHERE pinned = 1"
        elif filter_name == "other":
            query += " WHERE pinned = 0"

        query += " ORDER BY id DESC"

        rows = self.connection.execute(
            query,
            params,
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

    def get_note(self, note_id):
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

    def create_note(self, text):
        from datetime import datetime

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        cursor = self.connection.execute(
            """
            INSERT INTO notes (text, created_at, pinned)
            VALUES (?, ?, 0)
            """,
            (text, created_at),
        )
        self.connection.commit()
        return cursor.lastrowid

    def update_note(self, note_id, text):
        self.connection.execute(
            """
            UPDATE notes
            SET text = ?
            WHERE id = ?
            """,
            (text, note_id),
        )
        self.connection.commit()

    def delete_note(self, note_id):
        self.connection.execute(
            """
            DELETE FROM notes
            WHERE id = ?
            """,
            (note_id,),
        )
        self.connection.commit()

    def delete_all(self):
        self.connection.execute("DELETE FROM notes")
        self.connection.commit()

    def toggle_pin(self, note_id):
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

    def count_notes(self, filter_name="all"):
        if filter_name == "pinned":
            query = "SELECT COUNT(*) FROM notes WHERE pinned = 1"
        elif filter_name == "other":
            query = "SELECT COUNT(*) FROM notes WHERE pinned = 0"
        else:
            query = "SELECT COUNT(*) FROM notes"

        return self.connection.execute(query).fetchone()[0]

    def close(self):
        self.connection.close()
