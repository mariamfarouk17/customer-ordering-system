def test_menu_api_returns_categories():
    from app import app

    client = app.test_client()
    response = client.get("/api/menu")

    assert response.status_code == 200

    data = response.get_json()
    assert "categories" in data
    assert isinstance(data["categories"], list)