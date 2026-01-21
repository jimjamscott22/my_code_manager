import sqlite3
import os
from pathlib import Path
from typing import Optional

class Database:
    def __init__(self):
        self.data_dir = Path.home() / ".local" / "share" / "my-code-organizer"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "projects.db"
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        """Connect to the database and initialize schema if needed."""
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema."""
        cursor = self.conn.cursor()

        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                path TEXT NOT NULL UNIQUE,
                language TEXT,
                description TEXT,
                last_modified TIMESTAMP,
                is_favorite INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                color TEXT DEFAULT '#3584e4'
            )
        """)

        # Project-Tag junction table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS project_tags (
                project_id INTEGER,
                tag_id INTEGER,
                PRIMARY KEY (project_id, tag_id),
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)

        self.conn.commit()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def get_cursor(self):
        """Get a database cursor."""
        return self.conn.cursor()

# Global database instance
_db = Database()

def get_db():
    """Get the global database instance."""
    return _db
