def test_get_directors(client):
    res = client.get("/directors/")
    assert res.status_code == 200

def test_add_director(client):
    res = client.post("/directors/", json={"name": "Test Director"})
    assert res.status_code == 200
    assert res.json["name"] == "Test Director"

def test_get_director_by_id(client):
    create = client.post("/directors/", json={"name": "Dir X"}).json
    director_id = create["director_id"]
    res = client.get(f"/directors/{director_id}")
    assert res.status_code == 200
    assert res.json["director_id"] == director_id
