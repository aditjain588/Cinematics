def test_get_actors(client):
    res = client.get("/actors/")
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_add_actor(client):
    res = client.post("/actors/", json={"name": "Test Actor"})
    assert res.status_code == 200
    assert res.json["name"] == "Test Actor"

def test_get_actor_by_id(client):
    # Create first
    create = client.post("/actors/", json={"name": "Actor X"}).json
    actor_id = create["actor_id"]
    res = client.get(f"/actors/{actor_id}")
    assert res.status_code == 200
    assert res.json["actor_id"] == actor_id

def test_delete_actor(client):
    # Create first
    create = client.post("/actors/", json={"name": "Actor Y"}).json
    actor_id = create["actor_id"]
    res = client.delete(f"/actors/{actor_id}")
    assert res.status_code == 204
