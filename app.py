import sqlite3
import hashlib
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

DB_NAME = 'urls.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS urls_entry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_url TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect(DB_NAME)


def short_id_exists(short_id: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM urls_entry WHERE short_url = ?", (short_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def generate_short_id(long_url: str) -> str:
    salt = 0
    while True:
        digest = hashlib.md5(f"{long_url}{salt}".encode()).hexdigest()
        for length in range(4, 7):
            candidate = digest[:length]
            if not short_id_exists(candidate):
                return candidate
        salt += 1


def insert_url(long_url: str, short_id: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls_entry (long_url, short_url) VALUES (?, ?)",
        (long_url, short_id),
    )
    conn.commit()
    conn.close()


def fetch_long_url(short_id: str) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls_entry WHERE short_url = ?", (short_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None


def increment_click(short_id: str) -> None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls_entry SET clicks = clicks + 1 WHERE short_url = ?",
        (short_id,),
    )
    conn.commit()
    conn.close()


class URLRequest(BaseModel):
    url: str


class URLResponse(BaseModel):
    short_url: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.post("/shorten", response_model=URLResponse)
def create_short_url(payload: URLRequest):
    long_url = payload.url
    short_id = generate_short_id(long_url)
    insert_url(long_url, short_id)
    base_url = "http://localhost:8000"
    return URLResponse(short_url=f"{base_url}/{short_id}")


@app.get("/{short_id}")
def redirect(short_id: str):
    long_url = fetch_long_url(short_id)
    if not long_url:
        raise HTTPException(status_code=404, detail="URL not found")
    increment_click(short_id)
    return RedirectResponse(long_url)
