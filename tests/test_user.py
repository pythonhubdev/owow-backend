# async def test_create_user(client, clean_db):
#     response = await client.post("/v1/users", json={"username": "testuser", "password": "testpassword"})
#     assert response.status_code == 201
#     data = response.json()
#     assert data["data"]["username"] == "testuser"
#     assert "password" not in data["data"]
