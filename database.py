import os
import datetime
import psycopg2

from dotenv import load_dotenv

load_dotenv()

CREATE_MOVIES_TABLE = """
    CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);"""

CREATE_USERS_TABLE = """
    CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);"""

CREATE_WATCHED_TABLE = """
    CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY(user_username) REFERENCES users(username),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s);"
INSERT_USER = "INSERT INTO users (username) VALUES (%s);"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > %s;"
SELECT_WATCHED_MOVIES = """
    SELECT movies.* FROM movies
    JOIN watched ON movies.id = watched.movie_id
    JOIN users ON users.username = watched.user_username
    WHERE users.username = %s;
"""
INSERT_WATCHED_MOVIE = "INSERT INTO watched (user_username, movie_id) VALUES (%s, %s);"
SEARCH_MOVIES = "SELECT * FROM movies WHERE title LIKE %s;"
CREATE_RELEASE_INDEX = "CREATE INDEX IF NOT EXISTS idx_movies_release ON movies(release_timestamp);"

connection = psycopg2.connect(os.environ["DATABASE_URL"])


def create_tables():
    """Creates the new tables in the SQL database and creates an index on the movies table"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_MOVIES_TABLE)
            cursor.execute(CREATE_USERS_TABLE)
            cursor.execute(CREATE_WATCHED_TABLE)
            cursor.execute(CREATE_RELEASE_INDEX)


def add_user(username):
    """Inserts a new user into the users table"""
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_USER, (username,))


def add_movie(title, release_timestamp):
    """
    Adds a new movie to the movies table
    :param title: Movie title
    :param release_timestamp: Movie release date
    :return: None
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIES, (title, release_timestamp))


def get_movies(upcoming=False):
    """
    Grabs all movies from the movies table
    :param upcoming: True or False. Retrieves all movies if false, only upcoming movies if true.
    :return: Cursor pointing to the first row returned
    """
    with connection:
        with connection.cursor() as cursor:
            if upcoming:
                today_timestamp = datetime.datetime.today().timestamp()
                # argument must be a tuple hence the comma after today_timestamp
                cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,))
            else:
                cursor.execute(SELECT_ALL_MOVIES)
            return cursor.fetchall()


def search_movies(search_term):
    """
    Allows the user to search the movies table
    :param search_term: Search keywords (e.g., portion of a movie title)
    :return: Cursor pointing to the first row returned
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_MOVIES, (f"%{search_term}%",))
            return cursor.fetchall()


def watch_movie(username, movie_id):
    """
    Inserts a movie into the watched table
    :param username: Username
    :param movie_id: Movie ID as indicated in the movies table
    :return: None
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_WATCHED_MOVIE, (username, movie_id))


def get_watched_movies(username):
    """
    Runs SQL query to grab the watched movies table
    :param username: Username
    :return: Cursor pointing to the first row returned
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_WATCHED_MOVIES, (username,))
            return cursor.fetchall()
