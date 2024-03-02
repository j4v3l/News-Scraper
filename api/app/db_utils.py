from database.database import get_db_cursor, article_exists


def get_all_articles():
    """Get all articles"""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM articles;")
        result = cursor.fetchall()
        return result


def get_articles_by_category(category: str):
    """Get articles by category"""
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE categories LIKE ?"
        cursor.execute(query, ("%" + category + "%",))
        result = cursor.fetchall()
        return result


def get_article(permalink: str):
    """Get article by permalink"""
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM articles WHERE permalink = %s;", (permalink,))
        result = cursor.fetchone()
        return result
