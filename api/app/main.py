"""Main file for the API"""
from fastapi import FastAPI

from database.database import get_db_cursor, article_exists


app = FastAPI()


@app.get("/articles/{permalink}")
def read_article(permalink: str):
    """Get article by permalink

    Args:
        permalink (str): permalink of the article

    Returns:
        dict: article details
    """
    with get_db_cursor() as cursor:
        if article_exists(permalink):
            cursor.execute("SELECT * FROM articles WHERE permalink = %s;", (permalink,))
            result = cursor.fetchone()
            return result
        return {"error": "Article not found"}


# Display all articles
@app.get("/articles")
def read_articles():
    """Get all articles

    Returns:
        dict: all articles
    """
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM articles;")
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Display articles based on category
@app.get("/articles/category/{category}")
def read_articles_cat(category: str):
    """Get articles by category

    Args:
        category (str): category of the article

    Returns:
        dict: articles in the category
    """
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE categories LIKE ?"
        cursor.execute(query, ("%" + category + "%",))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Display articles based on date
@app.get("/articles/date/{date}")
def read_articles_date(date: str):
    """Get articles by date

    Args:
        date (str): date of the article

    Returns:
        dict: articles on the date
    """
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM articles WHERE date = %s;", (date,))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Display articles based on date and category
@app.get("/articles/date/{date}/category/{category}")
def read_articles_date_cat(date: str, category: str):
    """Get articles by date and category

    Args:
        date (str): date of the article
        category (str): category of the article

    Returns:
        dict: articles on the date and category
    """
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE date = ? AND categories LIKE ?"
        cursor.execute(query, (date, "%" + category + "%"))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Search articles based on title
@app.get("/articles/search/{title}")
def read_articles_title(title: str):
    """Search articles by title

    Args:
        title (str): title of the article

    Returns:
        dict: articles with the title
    """
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE title LIKE ?"
        cursor.execute(query, ("%" + title + "%",))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Search articles based on body
@app.get("/articles/search/body/{body}")
def read_articles_body(body: str):
    """Search articles by body

    Args:
        body (str): body of the article

    Returns:
        dict: articles with the body
    """
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE body LIKE ?"
        cursor.execute(query, ("%" + body + "%",))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


# Search articles based on a word
@app.get("/articles/search/word/{word}")
def read_articles_word(word: str):
    """Search articles by a word

    Args:
        word (str): word in the article

    Returns:
        dict: articles with the word
    """
    with get_db_cursor() as cursor:
        query = "SELECT * FROM articles WHERE title LIKE ? OR body LIKE ?"
        cursor.execute(query, ("%" + word + "%", "%" + word + "%"))
        result = cursor.fetchall()
        # return results in a more readable format
        return {"articles": result}


@app.get("/robots.txt")
def read_robots():
    """robots.txt

    Returns:
        str: robots.txt
    """
    return "User-agent: *\nDisallow: /"

@app.get("/")
def read_root():
    """Root path

    Returns:
        dict: Hello Javel
    """
    return {"Hello": "Javel"}
