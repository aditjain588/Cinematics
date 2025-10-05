from flask import request
from flask_restx import Namespace, Resource, fields
from models.actors_model import Actor
from models.movies_model import Movie
from db.connection import get_connection

# Namespace for actor routes
ns = Namespace("Actors", description="Operations related to actors")

# Swagger models
actor_summary = ns.model("ActorSummary", {
    "actor_id": fields.Integer,
    "name": fields.String
})

movie_summary = ns.model("MovieSummary", {
    "movie_id": fields.Integer,
    "title": fields.String,
    "release_year": fields.Integer
})

actor_detail = ns.inherit("ActorDetail", actor_summary, {
    "movies": fields.List(fields.Nested(movie_summary))
})

actor_input = ns.model("ActorInput", {
    "name": fields.String(required=True)
})


# Route: /actors/
@ns.route("/")
class ActorList(Resource):
    @ns.doc(params={"movie_id": "Filter actors by a specific movie"})
    @ns.marshal_list_with(actor_detail)
    def get(self):
        movie_id = request.args.get("movie_id")
        actors = Actor.get_all(movie_id)

        # Attach movies for each actor
        for actor in actors:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.movie_id, m.title, m.release_year, m.director_id
                FROM movies m
                JOIN actors_movie am ON m.movie_id = am.movie_id
                WHERE am.actor_id=%s
            """, (actor.actor_id,))

            rows = cursor.fetchall()
            movie_list = []
            for row in rows:
                movie = Movie(*row)
                movie_list.append(movie)
            actor.movies = movie_list

            cursor.close()
            conn.close()

        return actors

    @ns.expect(actor_input, validate=True)
    @ns.marshal_with(actor_detail, code=201)
    def post(self):
        data = request.json
        name = data.get("name")
        return Actor.add(name)


# Route: /actors/<actor_id>
@ns.route("/<int:actor_id>")
@ns.response(404, "Actor not found")
class ActorDetail(Resource):
    @ns.marshal_with(actor_detail)
    def get(self, actor_id):
        actor = Actor.get_by_id(actor_id)
        if not actor:
            ns.abort(404, "Actor not found")

        # Attach movies for that actor
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT m.movie_id, m.title, m.release_year, m.director_id
            FROM movies m
            JOIN actors_movie am ON m.movie_id = am.movie_id
            WHERE am.actor_id=%s
        """, (actor.actor_id,))

        rows = cursor.fetchall()
        movie_list = []
        for row in rows:
            movie = Movie(*row)
            movie_list.append(movie)
        actor.movies = movie_list

        cursor.close()
        conn.close()

        return actor

    def delete(self, actor_id):
        actor = Actor.get_by_id(actor_id)
        if not actor:
            ns.abort(404, "Actor not found")

        Actor.delete(actor_id)
        return {"message": "Deleted"}, 204
