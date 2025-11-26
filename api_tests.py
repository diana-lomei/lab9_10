import requests # type: ignore

BASE_URL = "https://jsonplaceholder.typicode.com"

# --- CREATE POST ---
post_data = {"title": "Test Post", "body": "Hello World", "userId": 1}
res = requests.post(f"{BASE_URL}/posts", json=post_data)
post_id = res.json()["id"]
assert res.status_code == 201

# --- READ POST ---
res = requests.get(f"{BASE_URL}/posts/{post_id}")
assert res.status_code == 200

# --- UPDATE POST ---
update_data = {"title": "Updated Post"}
res = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
assert res.status_code == 200

# --- DELETE POST ---
res = requests.delete(f"{BASE_URL}/posts/{post_id}")
assert res.status_code == 200

# --- ERROR CASES ---
res = requests.get(f"{BASE_URL}/posts/999999")
assert res.status_code == 404

res = requests.post(f"{BASE_URL}/posts", json={"title": ""})
assert res.status_code in [400, 201]

print("All API tests passed!")
