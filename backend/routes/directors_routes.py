from flask import request
from flask_restx import Namespace, Resource, fields
from models.directors_model import Director


# Namespace for director routes
ns = Namespace("Directors", description="Operations related to directors")

# Swagger models
director_summary = ns.model("DirectorSummary", {
    "director_id": fields.Integer,
    "name": fields.String
})

movie_summary = ns.model("MovieSummary", {
    "movie_id": fields.Integer,
    "title": fields.String,
    "release_year": fields.Integer
})

director_detail = ns.inherit("DirectorDetail", director_summary, {
    "movies": fields.List(fields.Nested(movie_summary))
})

director_input = ns.model("DirectorInput", {
    "name": fields.String(required=True)
})

# Route: /directors/
@ns.route("/")
class DirectorList(Resource):
    @ns.doc(params={"movie_id": "Filter by a specific movie", "genre_id": "Filter by genre"})
    @ns.marshal_list_with(director_detail)
    def get(self):
        movie_id = request.args.get("movie_id")
        genre_id = request.args.get("genre_id")

        directors = Director.get_all(movie_id, genre_id)

        # Add movies for each director
        for director in directors:
            director.movies = director.get_movies()

        return directors

    @ns.expect(director_input, validate=True)
    @ns.marshal_with(director_detail, code=201)
    def post(self):
        data = request.json
        return Director.add(data["name"])


# Route: /directors/<director_id>
@ns.route("/<int:director_id>")
@ns.response(404, "Director not found")
class DirectorDetail(Resource):
    @ns.marshal_with(director_detail)
    def get(self, director_id):
        director = Director.get_by_id(director_id)
        if not director:
            ns.abort(404, "Director not found")

        # Attach movies
        director.movies = director.get_movies()
        return director

    def delete(self, director_id):
        director = Director.get_by_id(director_id)
        if not director:
            ns.abort(404, "Director not found")

        Director.delete(director_id)
        return {"message": "Deleted"}, 204
