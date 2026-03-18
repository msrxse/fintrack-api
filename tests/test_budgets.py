def test_create_budget(client, auth_headers):
  category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

  response = client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers)

  assert response.status_code == 200

  data = response.json()
  assert data["limit_amount"] == "20.00"
  assert data["period"] == "weekly"
  assert data["category"]["id"] == category["id"]

def test_update_category(client, auth_headers):
  category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

  budget = client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers).json()

  response = client.put(f"/budgets/{budget['id']}",json={
    "limit_amount":"40.00"
  }, headers=auth_headers)
  assert response.status_code == 200

  data = response.json()
  assert data["limit_amount"] == "40.00"
  assert data["period"] == "weekly"
  assert data["category"]["id"] == category["id"]


def test_get_budgets(client, auth_headers):
  category = client.post("/categories/", json={
      "name": "Food",
      "type": "expense",
    }, headers=auth_headers).json()

  client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers).json()

  response = client.get("/budgets/", headers=auth_headers)
  assert response.status_code == 200

  data = response.json()
  assert len(data) == 1
  assert data[0]["limit_amount"] == "20.00"
  assert data[0]["period"] == "weekly"
  assert data[0]["category"]["id"] == category["id"]

def test_get_budget(client, auth_headers):
  category = client.post("/categories/", json={
    "name": "Food",
    "type": "expense",
  }, headers=auth_headers).json()

  budget = client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers).json()

  response = client.get(f"/budgets/{budget['id']}", headers=auth_headers)
  assert response.status_code == 200

  data = response.json()
  assert data["limit_amount"] == "20.00"
  assert data["period"] == "weekly"
  assert data["category"]["id"] == category["id"]

def test_delete_budget(client, auth_headers):
  category = client.post("/categories/", json={
    "name": "Food",
    "type": "expense",
  }, headers=auth_headers).json()

  db_budget = client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers).json()

  response = client.delete(f"/budgets/{db_budget['id']}", headers=auth_headers)
  assert response.status_code == 200

  gone = client.get(f"/budgets/{db_budget['id']}", headers=auth_headers)
  assert gone.status_code == 404


def test_no_repeated_budgets(client, auth_headers):
  category = client.post("/categories/", json={
    "name": "Food",
    "type": "expense",
  }, headers=auth_headers).json()

  client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers)

  response = client.post("/budgets/", json={
    "category_id": category["id"],
    "limit_amount": "20.00",
    "period": "weekly",
  }, headers=auth_headers)

  assert response.status_code == 409
