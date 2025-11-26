import requests # type: ignore

BASE_URL = "http://localhost:5000"

def test_create_user():
    res = requests.post(f"{BASE_URL}/users", json={"name": "Charlie", "age": 22})
    assert res.status_code == 201
    assert res.json()["name"] == "Charlie"

def test_get_user():
    res = requests.post(f"{BASE_URL}/users", json={"name": "Diana", "age": 28})
    uid = res.json()["id"]
    res = requests.get(f"{BASE_URL}/users/{uid}")
    assert res.status_code == 200
    assert res.json()["name"] == "Diana"

def test_update_user():
    res = requests.post(f"{BASE_URL}/users", json={"name": "Eve", "age": 35})
    uid = res.json()["id"]
    res = requests.put(f"{BASE_URL}/users/{uid}", json={"name": "Eve Updated", "age": 36})
    assert res.status_code == 200
    assert res.json()["name"] == "Eve Updated"

def test_delete_user():
    res = requests.post(f"{BASE_URL}/users", json={"name": "Frank", "age": 40})
    uid = res.json()["id"]
    res = requests.delete(f"{BASE_URL}/users/{uid}")
    assert res.status_code == 200
