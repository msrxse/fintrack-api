def test_spending_by_category(client, auth_headers, test_account):
    category = client.post("/categories/", json={
        "name": "Food",
        "type": "expense",
    }, headers=auth_headers).json()
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-03-12",
        "type":"expense",
        "amount": "70.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-03-11",
        "type":"expense",
        "amount": "5.00",
        "description": "Bread",
    }, headers=auth_headers)

    response = client.get("/analytics/spending-by-category?type=expense", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    totals = {item["category_name"]: item["total"] for item in data}
    assert totals["Food"] == "75.00"

def test_monthly_summary(client, auth_headers, test_account):
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-12",
        "type":"expense",
        "amount": "70.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-11",
        "type":"income",
        "amount": "5.00",
        "description": "Napkin",
    }, headers=auth_headers)

    response = client.get("/analytics/monthly-summary", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()

    assert data[0]["expenses"] == "70.00"
    assert data[0]["income"] == "5.00"

def test_top_merchants(client, auth_headers, test_account):
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-12",
        "type":"expense",
        "merchant": "TopMarket",
        "amount": "70.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-11",
        "type":"income",
        "merchant": "LessMarket",
        "amount": "5.00",
        "description": "Napkin",
    }, headers=auth_headers)

    response = client.get("/analytics/top-merchants", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data[0]["merchant"] == "TopMarket"
    assert data[0]["total"] == "70.00"
    assert data[0]["transaction_count"] == 1


def test_budget_status(client, auth_headers, test_account):
    category = client.post("/categories/", json={
        "name": "Food",
        "type": "expense",
    }, headers=auth_headers).json()
    client.post("/budgets/", json={
        "category_id": category["id"],
        "limit_amount": "200.00",
        "period": "monthly",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-03-12",
        "type":"expense",
        "amount": "70.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-03-11",
        "type":"expense",
        "amount": "5.00",
        "description": "Bread",
    }, headers=auth_headers)

    response = client.get("/analytics/budget-status", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data[0]["category_name"] == "Food"
    assert data[0]["limit_amount"] == "200.00"
    assert data[0]["actual_spent"] == "75.00"
    assert data[0]["remaining"] == "125.00"


def test_cash_flow(client, auth_headers, test_account):
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-12",
        "type":"expense",
        "amount": "70.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "date": "2026-03-11",
        "type":"expense",
        "amount": "15.00",
        "description": "Napkins",
    }, headers=auth_headers)

    response = client.get("/analytics/cash-flow", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data[-1]["running_balance"] == "85.00"



def test_trends(client, auth_headers, test_account):
    category = client.post("/categories/", json={
        "name": "Food",
        "type": "expense",
    }, headers=auth_headers).json()
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-03-11",
        "type":"expense",
        "amount": "200.00",
        "description": "Lunch",
    }, headers=auth_headers)
    client.post("/transactions/", json={
        "account_id": test_account["id"],
        "category_id":category["id"],
        "date": "2026-02-11",
        "type":"expense",
        "amount": "100.00",
        "description": "Lunch",
    }, headers=auth_headers)

    response = client.get("/analytics/trends", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert data[1]["change_pct"] == "100.00"