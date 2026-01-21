from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from .database import get_db

@dataclass
class Project:
    id: Optional[int]
    name: str
    path: str
    language: Optional[str] = None
    description: Optional[str] = None
    last_modified: Optional[datetime] = None
    is_favorite: bool = False
    created_at: Optional[datetime] = None

    @staticmethod
    def add(name: str, path: str, language: Optional[str] = None,
            description: Optional[str] = None) -> 'Project':
        """Add a new project to the database."""
        db = get_db()
        cursor = db.get_cursor()

        # Get last modified time from filesystem
        path_obj = Path(path)
        last_modified = datetime.fromtimestamp(path_obj.stat().st_mtime) if path_obj.exists() else None

        cursor.execute("""
            INSERT INTO projects (name, path, language, description, last_modified)
            VALUES (?, ?, ?, ?, ?)
        """, (name, path, language, description, last_modified))

        db.conn.commit()

        project_id = cursor.lastrowid
        return Project.get_by_id(project_id)

    @staticmethod
    def get_all() -> List['Project']:
        """Get all projects from the database."""
        db = get_db()
        cursor = db.get_cursor()

        cursor.execute("""
            SELECT * FROM projects ORDER BY last_modified DESC
        """)

        projects = []
        for row in cursor.fetchall():
            projects.append(Project._from_row(row))

        return projects

    @staticmethod
    def get_by_id(project_id: int) -> Optional['Project']:
        """Get a project by ID."""
        db = get_db()
        cursor = db.get_cursor()

        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()

        return Project._from_row(row) if row else None

    @staticmethod
    def delete(project_id: int):
        """Delete a project from the database."""
        db = get_db()
        cursor = db.get_cursor()

        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        db.conn.commit()

    @staticmethod
    def search(query: str = "", language: Optional[str] = None,
               favorites_only: bool = False) -> List['Project']:
        """Search projects with optional filters."""
        db = get_db()
        cursor = db.get_cursor()

        sql = "SELECT * FROM projects WHERE 1=1"
        params = []

        if query:
            sql += " AND (name LIKE ? OR path LIKE ? OR description LIKE ?)"
            like_query = f"%{query}%"
            params.extend([like_query, like_query, like_query])

        if language:
            sql += " AND language = ?"
            params.append(language)

        if favorites_only:
            sql += " AND is_favorite = 1"

        sql += " ORDER BY last_modified DESC"

        cursor.execute(sql, params)

        projects = []
        for row in cursor.fetchall():
            projects.append(Project._from_row(row))

        return projects

    @staticmethod
    def toggle_favorite(project_id: int) -> bool:
        """Toggle favorite status and return new state."""
        db = get_db()
        cursor = db.get_cursor()

        cursor.execute("SELECT is_favorite FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        if not row:
            return False

        new_state = not bool(row['is_favorite'])
        cursor.execute("UPDATE projects SET is_favorite = ? WHERE id = ?",
                      (int(new_state), project_id))
        db.conn.commit()

        return new_state

    @staticmethod
    def get_languages() -> List[str]:
        """Get list of unique languages from all projects."""
        db = get_db()
        cursor = db.get_cursor()

        cursor.execute("""
            SELECT DISTINCT language FROM projects
            WHERE language IS NOT NULL AND language != ''
            ORDER BY language
        """)

        return [row['language'] for row in cursor.fetchall()]

    @staticmethod
    def _from_row(row) -> 'Project':
        """Create a Project instance from a database row."""
        return Project(
            id=row['id'],
            name=row['name'],
            path=row['path'],
            language=row['language'],
            description=row['description'],
            last_modified=datetime.fromisoformat(row['last_modified']) if row['last_modified'] else None,
            is_favorite=bool(row['is_favorite']),
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else None
        )
