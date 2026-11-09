
import sqlite3
import hashlib
import secrets
import hmac
import re

from pathlib import Path
from contextlib import closing
from datetime import datetime, timezone


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "users.db"

PASSWORD_ITERATIONS = 600_000


def get_connection():

    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_auth_db():

    with closing(get_connection()) as conn:

        with conn:

            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (

                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,

                    name TEXT NOT NULL,

                    email TEXT NOT NULL UNIQUE COLLATE NOCASE,

                    password_hash TEXT NOT NULL,

                    password_salt TEXT NOT NULL,

                    created_at TEXT NOT NULL

                )
                """
            )


def hash_password(password, salt=None):

    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_ITERATIONS
    )

    return password_hash.hex(), salt.hex()


def verify_password(password, stored_hash, stored_salt):

    salt = bytes.fromhex(stored_salt)

    calculated_hash, _ = hash_password(
        password,
        salt
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_hash
    )


def validate_signup(name, email, password):

    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise ValueError("Please enter your full name.")

    if len(name) > 80:
        raise ValueError("Name must be 80 characters or fewer.")

    if not re.fullmatch(
        r"[^@\s]+@[^@\s]+\.[^@\s]+",
        email
    ):
        raise ValueError("Please enter a valid email address.")

    if len(email) > 254:
        raise ValueError("Email address is too long.")

    if len(password) < 8:
        raise ValueError(
            "Password must contain at least 8 characters."
        )

    return name, email


def register_user(name, email, password):

    name, email = validate_signup(
        name,
        email,
        password
    )

    password_hash, password_salt = hash_password(password)

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    try:

        with closing(get_connection()) as conn:

            with conn:

                cursor = conn.execute(
                    """
                    INSERT INTO users (
                        name,
                        email,
                        password_hash,
                        password_salt,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        password_hash,
                        password_salt,
                        created_at
                    )
                )

                user_id = cursor.lastrowid

        return {
            "user_id": user_id,
            "name": name,
            "email": email,
            "created_at": created_at
        }

    except sqlite3.IntegrityError:

        raise ValueError(
            "An account with this email already exists."
        )


def authenticate_user(email, password):

    email = email.strip().lower()

    with closing(get_connection()) as conn:

        user = conn.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if user is None:
        return None

    password_valid = verify_password(
        password,
        user["password_hash"],
        user["password_salt"]
    )

    if not password_valid:
        return None

    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "created_at": user["created_at"]
    }


def get_user_by_id(user_id):

    with closing(get_connection()) as conn:

        user = conn.execute(
            """
            SELECT
                user_id,
                name,
                email,
                created_at
            FROM users
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    if user is None:
        return None

    return dict(user)
