from pathlib import Path
from datetime import datetime
import sqlite3
import pandas as pd

DB_PATH = Path(__file__).with_name("cbr_cases.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS cases (
    patient TEXT PRIMARY KEY,
    mental_distress REAL NOT NULL,
    expectations INTEGER NOT NULL,
    pain_sites INTEGER NOT NULL,
    sleep TEXT NOT NULL,
    workability INTEGER NOT NULL,
    treatment_plan TEXT,
    pain_baseline REAL,
    pain_3m REAL,
    function_baseline REAL,
    function_3m REAL,
    mskhq_baseline REAL,
    mskhq_3m REAL,
    gpe INTEGER,
    successful_outcome INTEGER DEFAULT 0,
    created_at TEXT
)
"""

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    with connect() as con:
        con.execute(SCHEMA)
        con.commit()

def count_cases():
    with connect() as con:
        return int(con.execute("SELECT COUNT(*) FROM cases").fetchone()[0])

def load_cases():
    with connect() as con:
        df = pd.read_sql_query("SELECT * FROM cases ORDER BY patient", con)
    if not df.empty:
        df["successful_outcome"] = df["successful_outcome"].astype(bool)
    return df

def insert_case(case):
    cols = [
        "patient","mental_distress","expectations","pain_sites","sleep","workability",
        "treatment_plan","pain_baseline","pain_3m","function_baseline","function_3m",
        "mskhq_baseline","mskhq_3m","gpe","successful_outcome","created_at"
    ]
    vals = [
        case.get("patient"),
        float(case.get("mental_distress")),
        int(case.get("expectations")),
        int(case.get("pain_sites")),
        str(case.get("sleep")),
        int(case.get("workability")),
        case.get("treatment_plan"),
        case.get("pain_baseline"),
        case.get("pain_3m"),
        case.get("function_baseline"),
        case.get("function_3m"),
        case.get("mskhq_baseline"),
        case.get("mskhq_3m"),
        case.get("gpe"),
        int(bool(case.get("successful_outcome"))),
        case.get("created_at") or datetime.now().isoformat(timespec="seconds"),
    ]
    with connect() as con:
        con.execute(
            f"INSERT INTO cases ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})",
            vals
        )
        con.commit()

def next_patient_id():
    df = load_cases()
    nums = []
    for p in df["patient"].astype(str):
        try:
            nums.append(int(p.split("_")[-1]))
        except Exception:
            pass
    return f"Patient_{max(nums, default=0)+1}"
