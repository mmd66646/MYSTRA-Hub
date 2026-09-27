import sqlite3
from pathlib import Path
from typing import Optional


DATABASE_PATH = Path(__file__).parent / "mystra.db"


def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS personality_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            result_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (telegram_id)
                REFERENCES users(telegram_id)
        )
        """
    )

    connection.commit()
    connection.close()


def create_or_update_user(
    telegram_id: int,
    username: Optional[str],
    first_name: Optional[str],
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (
            telegram_id,
            username,
            first_name
        )
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id)
        DO UPDATE SET
            username = excluded.username,
            first_name = excluded.first_name,
            updated_at = CURRENT_TIMESTAMP
        """,
        (
            telegram_id,
            username,
            first_name,
        ),
    )

    connection.commit()
    connection.close()


def save_personality_result(
    telegram_id: int,
    result_json: str,
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO personality_results (
            telegram_id,
            result_json
        )
        VALUES (?, ?)
        """,
        (
            telegram_id,
            result_json,
        ),
    )

    connection.commit()
    connection.close()


def get_latest_personality_result(
    telegram_id: int,
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM personality_results
        WHERE telegram_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (telegram_id,),
    )

    result = cursor.fetchone()

    connection.close()

    return result


def get_personality_results(
    telegram_id: int,
):
    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM personality_results
        WHERE telegram_id = ?
        ORDER BY created_at DESC
        """,
        (telegram_id,),
    )

    results = cursor.fetchall()

    connection.close()

    return results