def test_create_category(client, auth_headers, test_user):
    response = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Food"
    assert data["type"] == "expense"
    assert not data["is_system"]
    assert data["user_id"] == test_user["id"]

def test_update_category(client, auth_headers):
    category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

    response = client.put(f"/categories/{category['id']}", json={
      "name": "Other",
    }, headers=auth_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Other"

def test_get_categories(client, auth_headers):
    client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers)
    client.post("/categories/", json={
      "name": "Other",
      "type": "expense",
    }, headers=auth_headers)
    categories = client.get("/categories/", headers=auth_headers)
    assert categories.status_code == 200

    data = categories.json()
    assert len(data) == 2

    assert data[0]["name"] == "Food"
    assert data[1]["name"] == "Other"

def test_get_category(client, auth_headers):
    category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

    response = client.get(f"/categories/{category['id']}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Food"
    assert data["type"] == "expense"


def test_delete_category(client, auth_headers):
    category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

    response = client.delete(f"/categories/{category['id']}", headers=auth_headers)
    assert response.status_code == 200

    gone = client.get(f"/categories/{category['id']}", headers=auth_headers)
    assert gone.status_code == 404
