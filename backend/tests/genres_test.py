def test_get_genres(client):
    res = client.get("/genres/")
    assert res.status_code == 200

def test_add_genre(client):
    res = client.post("/genres/", json={"name": "Action"})
    assert res.status_code == 200 
    data = res.json
    assert data["name"] == "Action"


def test_get_genre_by_id(client):
    create = client.post("/genres/", json={"name": "Drama"}).json
    genre_id = create["genre_id"]
    res = client.get(f"/genres/{genre_id}")
    assert res.status_code == 200
    assert res.json["genre_id"] == genre_id

def test_delete_genre(client):
    create = client.post("/genres/", json={"name": "Comedy"}).json
    genre_id = create["genre_id"]
    res = client.delete(f"/genres/{genre_id}")
    assert res.status_code == 204
