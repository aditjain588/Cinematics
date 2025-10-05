from db.connection import get_connection


class Actor:
    def __init__(self, actor_id, name):
        self.actor_id = actor_id
        self.name = name
        self.movies = []

    @classmethod
    def get_all(cls, movie_id=None):
        conn = get_connection()
        cursor = conn.cursor()

        if movie_id:
            cursor.execute("""
                SELECT a.actor_id, a.name
                FROM actors a
                JOIN actors_movie am ON a.actor_id = am.actor_id
                WHERE am.movie_id=%s
            """, (movie_id,))
        else:
            cursor.execute("SELECT actor_id, name FROM actors")

        rows = cursor.fetchall()
        actors = []
        for row in rows:
            actor_id = row[0]
            name = row[1]
            actor = Actor(actor_id, name)
            actors.append(actor)

        cursor.close()
        conn.close()
        return actors

    @classmethod
    def get_by_id(cls, actor_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT actor_id, name FROM actors WHERE actor_id=%s", (actor_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        actor_id = row[0]
        name = row[1]
        return Actor(actor_id, name)

    @classmethod
    def add(cls, name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO actors (name) VALUES (%s) RETURNING actor_id", (name,))
        actor_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return cls.get_by_id(actor_id)

    @classmethod
    def delete(cls, actor_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM actors_movie WHERE actor_id=%s", (actor_id,))
            cursor.execute("DELETE FROM actors WHERE actor_id=%s", (actor_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def get_movies(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.movie_id, m.title, m.release_year, m.director_id
            FROM movies m
            JOIN actors_movie am ON m.movie_id = am.movie_id
            WHERE am.actor_id=%s
        """, (self.actor_id,))

        from models.movies_model import Movie
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
