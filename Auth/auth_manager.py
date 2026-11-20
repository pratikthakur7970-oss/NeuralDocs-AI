
import re
import sqlite3
import secrets
import hashlib
import hmac

from pathlib import Path
from datetime import datetime, timezone
from contextlib import closing


# ==========================================
# DATABASE CONFIGURATION
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "data" / "neuraldocs_auth.db"

PBKDF2_ITERATIONS = 600_000


def get_connection():

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(
        str(DB_PATH),
        timeout=30
    )

    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    return conn


def current_time():

    return datetime.now(
        timezone.utc
    ).isoformat(timespec="seconds")


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

def init_db():

    with closing(get_connection()) as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                full_name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                password_hash TEXT NOT NULL,

                role TEXT NOT NULL DEFAULT 'user'
                    CHECK(role IN ('user', 'admin')),

                created_at TEXT NOT NULL,

                last_login TEXT

            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS login_events (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                email TEXT NOT NULL,

                login_at TEXT NOT NULL,

                FOREIGN KEY(user_id)
                REFERENCES users(id)
                ON DELETE CASCADE

            )
        """)

        conn.commit()


# ==========================================
# SECURE PASSWORD HASHING
# ==========================================

def hash_password(password):

    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS
    )

    return (
        f"pbkdf2_sha256$"
        f"{PBKDF2_ITERATIONS}$"
        f"{salt.hex()}$"
        f"{password_hash.hex()}"
    )


def verify_password(password, stored_hash):

    try:

        algorithm, iterations, salt, expected_hash = (
            stored_hash.split("$")
        )

        if algorithm != "pbkdf2_sha256":
            return False

        iterations = int(iterations)

        if iterations <= 0 or iterations > 2_000_000:
            return False

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            iterations
        )

        return hmac.compare_digest(
            calculated_hash.hex(),
            expected_hash
        )

    except (ValueError, TypeError):
        return False


# ==========================================
# REGISTER NEW USER
# ==========================================

def register_user(full_name, email, password):

    init_db()

    full_name = full_name.strip()
    email = email.strip().lower()

    if len(full_name) < 2:
        return False, "Please enter a valid full name."

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        return False, "Invalid email address."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    password_hash = hash_password(password)

    try:

        with closing(get_connection()) as conn:

            conn.execute("""
                INSERT INTO users (
                    full_name,
                    email,
                    password_hash,
                    role,
                    created_at
                )
                VALUES (?, ?, ?, 'user', ?)
            """, (
                full_name,
                email,
                password_hash,
                current_time()
            ))

            conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:

        return False, "An account with this email already exists."


# ==========================================
# AUTHENTICATE EXISTING USER
# ==========================================

def authenticate_user(email, password):

    init_db()

    email = email.strip().lower()

    with closing(get_connection()) as conn:

        user = conn.execute("""
            SELECT *
            FROM users
            WHERE email = ?
        """, (email,)).fetchone()

    if user is None:
        return None

    if not verify_password(
        password,
        user["password_hash"]
    ):
        return None

    login_time = current_time()

    with closing(get_connection()) as conn:

        conn.execute("""
            UPDATE users
            SET last_login = ?
            WHERE id = ?
        """, (
            login_time,
            user["id"]
        ))

        conn.execute("""
            INSERT INTO login_events (
                user_id,
                email,
                login_at
            )
            VALUES (?, ?, ?)
        """, (
            user["id"],
            user["email"],
            login_time
        ))

        conn.commit()

    return {
        "id": user["id"],
        "full_name": user["full_name"],
        "email": user["email"],
        "role": user["role"],
        "created_at": user["created_at"],
        "last_login": login_time
    }


# ==========================================
# ADMIN: GET ALL REGISTERED USERS
# ==========================================

def get_all_users():

    init_db()

    with closing(get_connection()) as conn:

        rows = conn.execute("""
            SELECT
                id,
                full_name,
                email,
                role,
                created_at,
                last_login
            FROM users
            ORDER BY created_at DESC
        """).fetchall()

        return [dict(row) for row in rows]


# ==========================================
# ADMIN: GET LOGIN HISTORY
# ==========================================

def get_login_history(limit=200):

    init_db()

    limit = max(1, min(int(limit), 1000))

    with closing(get_connection()) as conn:

        rows = conn.execute("""
            SELECT
                login_events.id,
                users.full_name,
                login_events.email,
                login_events.login_at
            FROM login_events
            INNER JOIN users
                ON users.id = login_events.user_id
            ORDER BY login_events.login_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

        return [dict(row) for row in rows]


# ==========================================
# PROMOTE REGISTERED USER TO ADMIN
# ==========================================

def promote_user_to_admin(email):

    init_db()

    with closing(get_connection()) as conn:

        cursor = conn.execute("""
            UPDATE users
            SET role = 'admin'
            WHERE email = ?
        """, (email.strip().lower(),))

        conn.commit()

        return cursor.rowcount > 0
