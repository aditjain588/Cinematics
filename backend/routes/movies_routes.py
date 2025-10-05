from flask import request
from flask_restx import Namespace, Resource, fields
from models.movies_model import Movie

# Namespace for movie-related routes
ns = Namespace("movies", description="Operations related to movies")

# --- Swagger models ---
actor_summary = ns.model("ActorSummary", {
    "actor_id": fields.Integer,
    "name": fields.String
})

genre_summary = ns.model("GenreSummary", {
    "genre_id": fields.Integer,
    "name": fields.String
})

director_summary = ns.model("DirectorSummary", {
    "director_id": fields.Integer,
    "name": fields.String
})

movie_detail = ns.model("MovieDetail", {
    "movie_id": fields.Integer,
    "title": fields.String,
    "release_year": fields.Integer,
    "director": fields.Nested(director_summary),
    "actors": fields.List(fields.Nested(actor_summary)),
    "genres": fields.List(fields.Nested(genre_summary))
})

movie_input = ns.model("MovieInput", {
    "title": fields.String(required=True),
    "release_year": fields.Integer(required=True),
    "director_id": fields.Integer(required=True),
    "genre_ids": fields.List(fields.Integer),
    "actor_ids": fields.List(fields.Integer)
})

# --- Routes ---
@ns.route("/")
class MovieList(Resource):
    @ns.doc(params={
        "genre_id": "Filter by genre id",
        "director_id": "Filter by director id",
        "release_year": "Filter by release year",
        "actor_id": "Filter by actor id"
    })
    @ns.marshal_list_with(movie_detail)
    def get(self):
        # Extract filter parameters from request
        filter_keys = ["genre_id", "director_id", "release_year", "actor_id"]
        filters = {}

        for key in filter_keys:
            value = request.args.get(key)
            if value:
                filters[key] = value

        # Fetch movies using filters
        movies = Movie.get_all(filters)

        # Convert movie objects to dictionaries for JSON response
        movie_dicts = []
        for movie in movies:
            movie_dicts.append(movie.__dict__)

        return movie_dicts

    @ns.expect(movie_input, validate=True)
    @ns.marshal_with(movie_detail, code=201)
    def post(self):
        data = request.json

        # Add a new movie
        title = data.get("title")
        release_year = data.get("release_year")
        director_id = data.get("director_id")
        genre_ids = data.get("genre_ids", [])
        actor_ids = data.get("actor_ids", [])

        movie = Movie.add(title, release_year, director_id, genre_ids, actor_ids)

        # Return newly created movie as dict
        return movie.__dict__


@ns.route("/<int:movie_id>")
@ns.response(404, "Movie not found")
class MovieDetail(Resource):
    @ns.marshal_with(movie_detail)
    def get(self, movie_id):
        movie = Movie.get_by_id(movie_id)
        if not movie:
            ns.abort(404, "Movie not found")

        print("Movie", movie)
        return movie.__dict__

    def delete(self, movie_id):
        movie = Movie.get_by_id(movie_id)
        if not movie:
            ns.abort(404, "Movie not found")

        Movie.delete(movie_id)
        return {"message": "Deleted"}, 204
