from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).parent / "consumer_intelligence.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS consumer_queries;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS retailer_availability;
        DROP TABLE IF EXISTS insight_clusters;
        DROP TABLE IF EXISTS recommended_actions;

        CREATE TABLE consumer_queries (
            id INTEGER PRIMARY KEY,
            text TEXT NOT NULL,
            channel TEXT NOT NULL,
            location TEXT NOT NULL,
            state TEXT NOT NULL,
            intent TEXT NOT NULL,
            product TEXT NOT NULL,
            retailer TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            priority TEXT NOT NULL,
            timestamp_label TEXT NOT NULL,
            created_at TEXT NOT NULL,
            resolved INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            sku TEXT NOT NULL,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            pack_type TEXT NOT NULL,
            health_positioning TEXT,
            core_region TEXT
        );

        CREATE TABLE retailer_availability (
            id INTEGER PRIMARY KEY,
            retailer TEXT NOT NULL,
            state TEXT NOT NULL,
            product_name TEXT NOT NULL,
            in_stock_score REAL NOT NULL,
            store_locator_accuracy REAL NOT NULL,
            promo_flag INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE insight_clusters (
            id INTEGER PRIMARY KEY,
            cluster_name TEXT NOT NULL,
            region TEXT NOT NULL,
            signal_volume INTEGER NOT NULL,
            opportunity_score INTEGER NOT NULL,
            notes TEXT NOT NULL
        );

        CREATE TABLE recommended_actions (
            id INTEGER PRIMARY KEY,
            pattern TEXT NOT NULL,
            evidence TEXT NOT NULL,
            action TEXT NOT NULL,
            owner TEXT NOT NULL,
            impact TEXT NOT NULL,
            metric TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()


def bulk_insert(table: str, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    conn = get_connection()
    cur = conn.cursor()
    columns = list(rows[0].keys())
    placeholders = ", ".join(["?"] * len(columns))
    col_sql = ", ".join(columns)
    values = [tuple(row[col] for col in columns) for row in rows]
    cur.executemany(
        f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})",
        values,
    )
    conn.commit()
    conn.close()
