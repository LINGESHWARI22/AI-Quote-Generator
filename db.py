# db.py
import sqlite3
import os
from datetime import datetime

DB_PATH = "quotes/quotes.db"


def init_db():
    os.makedirs("quotes", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_number TEXT,
            date TEXT,
            customer_name TEXT,
            phone TEXT,
            address TEXT,
            subtotal REAL,
            tax REAL,
            total REAL,
            pdf_path TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def save_quote(data: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO quotes (quote_number, date, customer_name, phone, address, subtotal, tax, total, pdf_path)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("quote_number"),
            data.get("date") or datetime.now().strftime("%Y-%m-%d %H:%M"),
            data.get("customer_name"),
            data.get("phone"),
            data.get("address"),
            data.get("subtotal"),
            data.get("tax"),
            data.get("total"),
            data.get("pdf_path"),
        ),
    )
    conn.commit()
    conn.close()


def list_quotes(limit=50):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT quote_number, date, customer_name, total, pdf_path FROM quotes ORDER BY id DESC LIMIT ?",
        (limit,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows
