from db.connection import get_connection
from models.movies_model import Movie


class Director:
    def __init__(self, director_id, name):
        self.director_id = director_id
        self.name = name
        self.movies = []

    @classmethod
    def get_all(cls, movie_id=None, genre_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT DISTINCT d.director_id, d.name FROM directors d"
        params = []

        if movie_id:
            query += " JOIN movies m ON d.director_id = m.director_id WHERE m.movie_id = %s"
            params.append(movie_id)
        elif genre_id:
            query += """ JOIN movies m ON d.director_id = m.director_id
                         JOIN movies_genres mg ON m.movie_id = mg.movie_id
                         WHERE mg.genre_id = %s"""
            params.append(genre_id)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()

        directors = []
        for row in rows:
            director_id = row[0]
            name = row[1]
            director = Director(director_id, name)
            directors.append(director)

        cursor.close()
        conn.close()
        return directors

    @classmethod
    def get_by_id(cls, director_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT director_id, name FROM directors WHERE director_id=%s", (director_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        director_id = row[0]
        name = row[1]
        return Director(director_id, name)

    @classmethod
    def add(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO directors (name) VALUES (%s) RETURNING director_id", (name,))
        director_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return cls.get_by_id(director_id)

    def get_movies(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie_id, title, release_year, director_id FROM movies WHERE director_id=%s", (self.director_id,))
        rows = cursor.fetchall()

        self.movies = []
        for row in rows:
            movie_id = row[0]
            title = row[1]
            release_year = row[2]
            director_id = row[3]
            movie = Movie(movie_id, title, release_year, director_id)
            self.movies.append(movie)

        cursor.close()
        conn.close()
        return self.movies
