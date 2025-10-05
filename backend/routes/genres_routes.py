from flask import request
from flask_restx import Namespace, Resource, fields
from models.genres_model import Genre


# Namespace for genre routes
ns = Namespace("Genres", description="Operations related to genres")

# Swagger models
genre_summary = ns.model("GenreSummary", {
    "genre_id": fields.Integer,
    "name": fields.String
})

movie_summary = ns.model("MovieSummary", {
    "movie_id": fields.Integer,
    "title": fields.String,
    "release_year": fields.Integer
})

genre_detail = ns.inherit("GenreDetail", genre_summary, {
    "movies": fields.List(fields.Nested(movie_summary))
})

genre_input = ns.model("GenreInput", {
    "name": fields.String(required=True)
})


# Route: /genres/
@ns.route("/")
class GenreList(Resource):
    @ns.doc(params={"movie_id": "Filter by a specific movie"})
    @ns.marshal_list_with(genre_detail)
    def get(self):
        movie_id = request.args.get("movie_id")

        # Fetch all genres (optionally filtered by movie)
        genres = Genre.get_all(movie_id)

        # Add movies to each genre
        for genre in genres:
            genre.movies = genre.get_movies()

        return genres

    @ns.expect(genre_input, validate=True)
    @ns.marshal_with(genre_detail, code=201)
    def post(self):
        data = request.json
        return Genre.add(data["name"])


@ns.route("/")
class GenreList(Resource):
    @ns.expect(genre_input, validate=True)
    @ns.marshal_with(genre_detail, code=201)
    def post(self):
        data = request.json
        return Genre.add(data["name"])


# Route: /genres/<genre_id>
@ns.route("/<int:genre_id>")
@ns.response(404, "Genre not found")
class GenreDetail(Resource):
    @ns.marshal_with(genre_detail)
    def get(self, genre_id):
        genre = Genre.get_by_id(genre_id)
        if not genre:
            ns.abort(404, "Genre not found")

        # Attach movies
        genre.movies = genre.get_movies()
        return genre

    def delete(self, genre_id):
        genre = Genre.get_by_id(genre_id)
        if not genre:
            ns.abort(404, "Genre not found")

        Genre.delete(genre_id)
        return {"message": "Deleted"}, 204
