def test_create_account(client, auth_headers):
    response = client.post("/accounts/", json={
        "name": "Test Checking",
        "type": "checking",
        "currency": "USD",
        "balance": "1000.00",
    }, headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Checking"
    assert data["type"] == "checking"
    assert data["currency"] == "USD"
    assert data["balance"] == "1000.00"

def test_update_account(client, auth_headers, test_account):
    response = client.put(f"/accounts/{test_account['id']}", json={
        "is_active": True,
    }, headers=auth_headers)

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Checking"
    assert data["type"] == "checking"
    assert data["currency"] == "USD"
    assert data["is_active"]

def test_get_accounts(client, auth_headers, test_account):
    response = client.get("/accounts/", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Checking"

def test_get_account(client, auth_headers, test_account):
    response = client.get(f"/accounts/{test_account['id']}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == test_account["id"]
    assert data["name"] == "Test Checking"


def test_delete_account(client, auth_headers, test_account):
    response = client.delete(f"/accounts/{test_account['id']}", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert not data["is_active"]
