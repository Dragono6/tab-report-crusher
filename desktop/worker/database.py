import sqlite3
from pathlib import Path

# The database will be created in the user's app data directory, managed by Tauri.
# For local development, we'll place it in the worker directory for simplicity.
# TODO: Integrate with Tauri's path resolver API to get the proper app data directory.
DB_PATH = Path(__file__).parent / "tab_crusher.sqlite"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_schema():
    """Creates the database schema if it doesn't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Profile table: Stores different sets of tolerances and settings.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        json_data TEXT NOT NULL, -- Storing tolerances as a JSON string
        version INTEGER NOT NULL
    );
    """)
    
    # Rules table: Stores user-defined YAML rules for the review process.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rules (
        id TEXT PRIMARY KEY,
        profile_id TEXT NOT NULL,
        yaml_rule TEXT NOT NULL,
        version INTEGER NOT NULL,
        FOREIGN KEY (profile_id) REFERENCES profiles (id)
    );
    """)

    # Runs table: Logs each time a report is reviewed.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id TEXT PRIMARY KEY,
        profile_id TEXT NOT NULL,
        file_hash TEXT NOT NULL, -- To detect re-runs of the same file
        result_json TEXT NOT NULL, -- The JSON output from the AI review
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (profile_id) REFERENCES profiles (id)
    );
    """)

    # Pending Updates table: Offline queue for syncing with the cloud API.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pending_updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        payload_json TEXT NOT NULL, -- The JSON payload to send to the API
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    conn.close()
    print("Database schema initialized successfully.", file=sys.stderr)
    
    # Populate default data if the database was just created
    populate_default_profile()

def populate_default_profile():
    """Inserts the default tolerance profile if no profiles exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM profiles")
    if cursor.fetchone() is None:
        import json
        import uuid

        default_tolerances = {
            "Supply": {"type": "percent", "value": 10},
            "Return": {"type": "percent", "value": 10},
            "Exhaust": {"type": "percent", "value": 15},
            "OA": {"type": "percent", "value": 5},
            "Coil_dT": {"type": "absolute", "value": 2, "unit": "F"}
        }
        
        profile_id = str(uuid.uuid4())
        
        cursor.execute(
            "INSERT INTO profiles (id, name, json_data, version) VALUES (?, ?, ?, ?)",
            (
                profile_id,
                "Manager Default",
                json.dumps(default_tolerances),
                1
            )
        )
        conn.commit()
        print("Inserted default tolerance profile.", file=sys.stderr)
        
    conn.close()

if __name__ == '__main__':
    # Allows running this script directly to initialize the database.
    import sys
    create_schema() 