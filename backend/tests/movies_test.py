def test_get_movies(client):
    res = client.get("/movies/")
    assert res.status_code == 200

def test_add_movie(client):
    # First, create director, actor, genre
    director = client.post("/directors/", json={"name": "Dir Test"}).json
    actor = client.post("/actors/", json={"name": "Actor Test"}).json
    genre = client.post("/genres/", json={"name": "Genre Test"}).json

    res = client.post("/movies/", json={
        "title": "Test Movie",
        "release_year": 2025,
        "director_id": director["director_id"],
        "actor_ids": [actor["actor_id"]],
        "genre_ids": [genre["genre_id"]]
    })
    assert res.status_code == 200
    assert res.json["title"] == "Test Movie"

def test_get_movie_by_id(client):
    director = client.post("/directors/", json={"name": "Dir X"}).json
    actor = client.post("/actors/", json={"name": "Actor X"}).json
    movie = client.post("/movies/", json={
        "title": "Movie X",
        "release_year": 2025,
        "director_id": director["director_id"],
        "actor_ids": [actor["actor_id"]],
        "genre_ids": []
    }).json
    res = client.get(f"/movies/{movie['movie_id']}")
    assert res.status_code == 200
    assert res.json["movie_id"] == movie["movie_id"]

def test_delete_movie(client):
    director = client.post("/directors/", json={"name": "Dir Y"}).json
    actor = client.post("/actors/", json={"name": "Actor Y"}).json
    movie = client.post("/movies/", json={
        "title": "Movie Y",
        "release_year": 2025,
        "director_id": director["director_id"],
        "actor_ids": [actor["actor_id"]],
        "genre_ids": []
    }).json
    res = client.delete(f"/movies/{movie['movie_id']}")
    assert res.status_code == 204
