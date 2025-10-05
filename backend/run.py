from flask import Flask, jsonify
from flask_restx import Api
from flask_cors import CORS
from routes.movies_routes import ns as movies_ns
from routes.actor_routes import ns as actors_ns
from routes.directors_routes import ns as directors_ns
from routes.genres_routes import ns as genres_ns

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(
    app,
    version="1.0",
    title="Cinematics API",
    description="Movies, Actors, Directors, Genres",
)

# Register namespaces
api.add_namespace(movies_ns, path="/movies")
api.add_namespace(actors_ns, path="/actors")
api.add_namespace(directors_ns, path="/directors")
api.add_namespace(genres_ns, path="/genres")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)