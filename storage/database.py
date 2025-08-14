"""SQLite storage for signals and user preferences."""
from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable, Optional

from config.config import DB_FILE

SCHEMA = """
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT,
    direction TEXT,
    price REAL,
    tp REAL,
    sl REAL,
    probability REAL,
    eta INTEGER,
    status TEXT DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS pairs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT,
    result TEXT
);
"""


class Database:
    def __init__(self, path: Path = DB_FILE) -> None:
        self.conn = sqlite3.connect(path)
        self.conn.executescript(SCHEMA)

    # -- signals ---------------------------------------------------------
    def add_signal(self, pair: str, direction: str, price: float, tp: float, sl: float,
                   probability: float, eta: int) -> int:
        cur = self.conn.cursor()
        cur.execute(
            """INSERT INTO signals(pair,direction,price,tp,sl,probability,eta)
            VALUES(?,?,?,?,?,?,?)""",
            (pair, direction, price, tp, sl, probability, eta),
        )
        self.conn.commit()
        return cur.lastrowid

    def update_signal_status(self, signal_id: int, status: str) -> None:
        self.conn.execute("UPDATE signals SET status=? WHERE id=?", (status, signal_id))
        self.conn.commit()

    def has_active_signal(self, pair: str) -> bool:
        cur = self.conn.execute(
            "SELECT 1 FROM signals WHERE pair=? AND status='ACTIVE' LIMIT 1", (pair,)
        )
        return cur.fetchone() is not None

    # -- pairs -----------------------------------------------------------
    def add_pair(self, pair: str) -> None:
        self.conn.execute("INSERT OR IGNORE INTO pairs(pair) VALUES(?)", (pair,))
        self.conn.commit()

    def get_pairs(self) -> Iterable[str]:
        cur = self.conn.execute("SELECT pair FROM pairs")
        return [r[0] for r in cur.fetchall()]

    # -- stats -----------------------------------------------------------
    def log_result(self, pair: str, result: str) -> None:
        self.conn.execute(
            "INSERT INTO stats(pair,result) VALUES(?,?)", (pair, result)
        )
        self.conn.commit()

