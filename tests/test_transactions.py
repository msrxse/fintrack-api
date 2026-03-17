def test_create_transaction(client, auth_headers, test_account):
    response = client.post("/transactions/", json={
        "account_id": test_account["id"],
        "amount": "50.00",
        "type": "expense",
        "date": "2026-03-16",
        "description": "Coffee",
    }, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == "50.00"
    assert data["description"] == "Coffee"
    assert data["account_id"] == test_account["id"]


def test_get_transaction(client, auth_headers, test_account):
    created = client.post("/transactions/", json={
        "account_id": test_account["id"],
        "amount": "25.00",
        "type": "expense",
        "date": "2026-03-16",
    }, headers=auth_headers).json()

    response = client.get(f"/transactions/{created['id']}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_transaction_not_found(client, auth_headers):
    response = client.get("/transactions/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_transaction(client, auth_headers, test_account):
    created = client.post("/transactions/", json={
        "account_id": test_account["id"],
        "amount": "30.00",
        "type": "expense",
        "date": "2026-03-16",
        "description": "Lunch",
    }, headers=auth_headers).json()

    response = client.put(f"/transactions/{created['id']}", json={
        "description": "Dinner",
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["description"] == "Dinner"


def test_delete_transaction(client, auth_headers, test_account):
    created = client.post("/transactions/", json={
        "account_id": test_account["id"],
        "amount": "15.00",
        "type": "expense",
        "date": "2026-03-16",
    }, headers=auth_headers).json()

    delete_response = client.delete(f"/transactions/{created['id']}", headers=auth_headers)
    assert delete_response.status_code == 200

    get_response = client.get(f"/transactions/{created['id']}", headers=auth_headers)
    assert get_response.status_code == 404
