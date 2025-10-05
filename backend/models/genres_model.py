from db.connection import get_connection
from models.movies_model import Movie


class Genre:
    def __init__(self, genre_id, name):
        self.genre_id = genre_id
        self.name = name
        self.movies = []

    @classmethod
    def get_all(cls, movie_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT DISTINCT g.genre_id, g.name FROM genres g"
        params = []
        if movie_id:
            query += " JOIN movies_genres mg ON g.genre_id = mg.genre_id WHERE mg.movie_id = %s"
            params.append(movie_id)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        genres = []
        for row in rows:
            genre_id = row[0]
            name = row[1]
            genre = Genre(genre_id, name)
            genres.append(genre)

        cursor.close()
        conn.close()
        return genres

    @classmethod
    def add(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO genres (name) VALUES (%s) RETURNING genre_id, name", (name,))
        row = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()

        genre_id = row[0]
        name = row[1]
        return Genre(genre_id, name)

    @classmethod
    def get_by_id(cls, genre_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT genre_id, name FROM genres WHERE genre_id = %s", (genre_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        genre_id = row[0]
        name = row[1]
        return Genre(genre_id, name)

    @classmethod
    def delete(cls, genre_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM genres WHERE genre_id = %s", (genre_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_movies(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.movie_id, m.title, m.release_year, m.director_id
            FROM movies m
            JOIN movies_genres mg ON m.movie_id = mg.movie_id
            WHERE mg.genre_id = %s
        """, (self.genre_id,))
        rows = cursor.fetchall()

        movies = []
        for row in rows:
            movie_id = row[0]
            title = row[1]
            release_year = row[2]
            director_id = row[3]
            movie = Movie(movie_id, title, release_year, director_id)
            movies.append(movie)

        cursor.close()
        conn.close()
        return movies
