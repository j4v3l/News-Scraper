"""This module contains functions for interacting with the SQLite database."""

import sqlite3
from contextlib import contextmanager
import os

# Path to your SQLite database file
DATABASE_PATH = os.path.join(os.getcwd(), "./storage/database.db")


@contextmanager
def get_db_connection():
    """Yields a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def get_db_cursor(commit=False):
    """Yields a database cursor and commits changes if commit is True."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            if commit:
                conn.commit()
        finally:
            cursor.close()


def create_articles_table():
    """Creates the articles table in the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                page_id INTEGER,
                date TEXT,
                title TEXT,
                body TEXT,
                categories TEXT,
                permalink TEXT UNIQUE,
                image_source TEXT
            );
        """
        )
        conn.commit()


def article_exists(permalink):
    """Returns True if an article with the given permalink exists in the database."""
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM articles WHERE permalink = ?)", (permalink,)
        )
        result = cursor.fetchone()
        return result[0] if result else False


def save_article_to_db(date, title, body, categories, permalink, img_src, page_num):
    """Saves the article details to the database."""
    if not article_exists(permalink):
        with get_db_cursor(commit=True) as cursor:
            cursor.execute(
                """
                INSERT INTO articles (date, title, body, categories, permalink, image_source, page_id)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
                (date, title, body, categories, permalink, img_src, page_num),
            )
        print(f"Article saved: {title}")
    else:
        print(f"Article already exists: {title}")


create_articles_table()
