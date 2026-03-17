def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New User",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["full_name"] == "New User"
    assert "id" in data
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    response = client.post("/auth/register", json={
        "email": "testuser@example.com",
        "password": "password123",
        "full_name": "Another User",
    })
    assert response.status_code == 409


def test_login_success(client, test_user):
    response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    response = client.post("/auth/login", json={
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "wrongpassword",
    })
    assert response.status_code == 401


def test_get_me_no_token(client):
    response = client.get("/auth/users/me")
    assert response.status_code == 403


def test_get_me_invalid_token(client):
    response = client.get("/auth/users/me", headers={"Authorization": "Bearer faketoken"})
    assert response.status_code == 401


def test_get_me_success(client, auth_headers):
    response = client.get("/auth/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert data["full_name"] == "Test User"
