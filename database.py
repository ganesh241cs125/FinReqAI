import sqlite3
import json
from pathlib import Path
from ..config import DATA_DIR

DB_PATH = DATA_DIR / "finreqai.db"

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = connect()
    con.executescript("""
    CREATE TABLE IF NOT EXISTS projects (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        domain TEXT NOT NULL,
        description TEXT NOT NULL,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS requirements (
        id TEXT PRIMARY KEY,
        project_id TEXT NOT NULL,
        data_json TEXT NOT NULL,
        FOREIGN KEY(project_id) REFERENCES projects(id)
    );

    CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        requirement_id TEXT NOT NULL,
        decision TEXT NOT NULL,
        comment TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        details_json TEXT,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id TEXT NOT NULL,
        artifact_type TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    );
    """)
    con.commit()
    con.close()

def save_project(project):
    con = connect()
    con.execute(
        "INSERT OR REPLACE INTO projects(id,name,domain,description,created_at) VALUES(?,?,?,?,?)",
        (project["id"], project["name"], project["domain"], project["description"], project["created_at"])
    )
    con.commit()
    con.close()

def save_requirements(project_id, requirements):
    con = connect()
    for r in requirements:
        con.execute(
            "INSERT OR REPLACE INTO requirements(id,project_id,data_json) VALUES(?,?,?)",
            (r["id"], project_id, json.dumps(r))
        )
    con.commit()
    con.close()

def save_artifact(project_id, artifact_type, content, created_at):
    con = connect()
    con.execute(
        "INSERT INTO artifacts(project_id,artifact_type,content,created_at) VALUES(?,?,?,?)",
        (project_id, artifact_type, content, created_at)
    )
    con.commit()
    con.close()

def save_audit(project_id, actor, action, details, created_at):
    con = connect()
    con.execute(
        "INSERT INTO audits(project_id,actor,action,details_json,created_at) VALUES(?,?,?,?,?)",
        (project_id, actor, action, json.dumps(details))
    )
    con.commit()
    con.close()

def save_approval(project_id, requirement_id, decision, comment, created_at):
    con = connect()
    con.execute(
        "INSERT INTO approvals(project_id,requirement_id,decision,comment,created_at) VALUES(?,?,?,?,?)",
        (project_id, requirement_id, decision, comment, created_at)
    )
    con.commit()
    con.close()

def list_projects():
    con = connect()
    rows = con.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    con.close()
    return [dict(r) for r in rows]

def get_requirements(project_id):
    con = connect()
    rows = con.execute("SELECT data_json FROM requirements WHERE project_id=?", (project_id,)).fetchall()
    con.close()
    return [json.loads(r["data_json"]) for r in rows]

def get_artifact(project_id, artifact_type):
    con = connect()
    row = con.execute(
        "SELECT content FROM artifacts WHERE project_id=? AND artifact_type=? ORDER BY id DESC LIMIT 1",
        (project_id, artifact_type)
    ).fetchone()
    con.close()
    return row["content"] if row else None

def get_audits(project_id):
    con = connect()
    rows = con.execute(
        "SELECT * FROM audits WHERE project_id=? ORDER BY id DESC", (project_id,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]
