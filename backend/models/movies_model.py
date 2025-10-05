from db.connection import get_connection


class Movie:
    def __init__(self, movie_id, title, release_year, director_id):
        self.movie_id = movie_id
        self.title = title
        self.release_year = release_year
        self.director_id = director_id
        self.actors = []
        self.genres = []
        self.director = None

    def fetch_relations(self):
        from models.actors_model import Actor
        from models.genres_model import Genre
        from models.directors_model import Director

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch actors
        cursor.execute("""
            SELECT a.actor_id, a.name
            FROM actors a
            JOIN actors_movie am ON a.actor_id = am.actor_id
            WHERE am.movie_id=%s
        """, (self.movie_id,))
        rows = cursor.fetchall()
        self.actors = []
        for row in rows:
            actor_id = row[0]
            name = row[1]
            actor = Actor(actor_id, name)
            self.actors.append(actor)

        # Fetch genres
        cursor.execute("""
            SELECT g.genre_id, g.name
            FROM genres g
            JOIN movies_genres mg ON g.genre_id = mg.genre_id
            WHERE mg.movie_id=%s
        """, (self.movie_id,))
        rows = cursor.fetchall()
        self.genres = []
        for row in rows:
            genre_id = row[0]
            name = row[1]
            genre = Genre(genre_id, name)
            self.genres.append(genre)

        # Fetch director
        cursor.execute("SELECT director_id, name FROM directors WHERE director_id=%s", (self.director_id,))
        row = cursor.fetchone()
        if row:
            director_id = row[0]
            name = row[1]
            self.director = Director(director_id, name)

        cursor.close()
        conn.close()

    @classmethod
    def get_all(cls, filters=None):
        filters = filters or {}
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT m.movie_id, m.title, m.release_year, m.director_id FROM movies m"
        joins = []
        conditions = []
        values = []

        if "genre_id" in filters:
            joins.append("JOIN movies_genres mg ON m.movie_id = mg.movie_id")
            conditions.append("mg.genre_id = %s")
            values.append(filters["genre_id"])
        if "actor_id" in filters:
            joins.append("JOIN actors_movie am ON m.movie_id = am.movie_id")
            conditions.append("am.actor_id = %s")
            values.append(filters["actor_id"])
        if "director_id" in filters:
            conditions.append("m.director_id = %s")
            values.append(filters["director_id"])
        if "release_year" in filters:
            conditions.append("m.release_year = %s")
            values.append(filters["release_year"])

        if joins:
            query += " " + " ".join(joins)
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, tuple(values))
        rows = cursor.fetchall()

        movies = []
        for row in rows:
            movie_id = row[0]
            title = row[1]
            release_year = row[2]
            director_id = row[3]
            movie = Movie(movie_id, title, release_year, director_id)
            movie.fetch_relations()
            movies.append(movie)

        cursor.close()
        conn.close()
        return movies

    @classmethod
    def get_by_id(cls, movie_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT movie_id, title, release_year, director_id FROM movies WHERE movie_id=%s", (movie_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if not row:
            return None

        movie_id = row[0]
        title = row[1]
        release_year = row[2]
        director_id = row[3]
        movie = Movie(movie_id, title, release_year, director_id)
        movie.fetch_relations()
        return movie

    @classmethod
    def add(cls, title, release_year, director_id, genre_ids=None, actor_ids=None):
        genre_ids = genre_ids or []
        actor_ids = actor_ids or []

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO movies (title, release_year, director_id) VALUES (%s, %s, %s) RETURNING movie_id",
            (title, release_year, director_id)
        )
        movie_id = cursor.fetchone()[0]

        for gid in genre_ids:
            cursor.execute("INSERT INTO movies_genres (movie_id, genre_id) VALUES (%s, %s)", (movie_id, gid))
        for aid in actor_ids:
            cursor.execute("INSERT INTO actors_movie (movie_id, actor_id) VALUES (%s, %s)", (movie_id, aid))

        conn.commit()
        cursor.close()
        conn.close()
        return cls.get_by_id(movie_id)

    @classmethod
    def delete(cls, movie_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM actors_movie WHERE movie_id=%s", (movie_id,))
        cursor.execute("DELETE FROM movies_genres WHERE movie_id=%s", (movie_id,))
        cursor.execute("DELETE FROM movies WHERE movie_id=%s", (movie_id,))
        conn.commit()
        cursor.close()
        conn.close()
