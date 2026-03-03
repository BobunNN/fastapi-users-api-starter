# Basic tests for the users router
import pytest
from fastapi.testclient import TestClient

from src.app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_read_users(client, superuser_token, regular_token):
    # Not authenticated
    resp = client.get("/v1/users")
    assert resp.status_code in (401, 403)
    # # As superuser
    # resp = client.get("/v1/users", headers={"Authorization": f"Bearer {superuser_token}"})
    # assert resp.status_code == 200
    # As regular user
    print(regular_token)
    resp = client.get("/v1/users", headers={"Authorization": f"Bearer {regular_token}"})
    assert resp.status_code == 401


# def test_read_user_me(client, superuser_token, regular_token):
# 	# Not authenticated
# 	resp = client.get("/v1/users/me")
# 	assert resp.status_code in (401, 403)
# 	# As superuser
# 	resp = client.get("/v1/users/me", headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code == 200
# 	# As regular user
# 	resp = client.get("/v1/users/me", headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code == 200


# def test_fetch_user(client, superuser_token, regular_token):
# 	# Not authenticated
# 	resp = client.get("/v1/users/admin@example.com")
# 	assert resp.status_code in (401, 403)
# 	# As superuser
# 	resp = client.get("/v1/users/admin@example.com", headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 404)
# 	# As regular user
# 	resp = client.get("/v1/users/admin@example.com", headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code == 403


# def test_create_user(client, superuser_token, regular_token):
# 	data = {
# 		"first_name": "Test",
# 		"last_name": "User",
# 		"email": "testuser@example.com",
# 		"password": "testpassword",
# 		"is_superuser": False
# 	}
# 	# Not authenticated
# 	resp = client.post("/v1/users", json=data)
# 	assert resp.status_code in (401, 403, 422)
# 	# As superuser
# 	resp = client.post("/v1/users", json=data, headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 201, 422)
# 	# As regular user
# 	resp = client.post("/v1/users", json=data, headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code == 403


# def test_update_user_me(client, superuser_token, regular_token):
# 	data = {
# 		"first_name": "Updated",
# 		"last_name": "User"
# 	}
# 	# Not authenticated
# 	resp = client.patch("/v1/users/me", json=data)
# 	assert resp.status_code in (401, 403, 422)
# 	# As superuser
# 	resp = client.patch("/v1/users/me", json=data, headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 422)
# 	# As regular user
# 	resp = client.patch("/v1/users/me", json=data, headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code in (200, 422)


# def test_patch_user(client, superuser_token, regular_token):
# 	data = {
# 		"first_name": "Patched",
# 		"last_name": "User"
# 	}
# 	# Not authenticated
# 	resp = client.patch("/v1/users/admin@example.com", json=data)
# 	assert resp.status_code in (401, 403, 404, 422)
# 	# As superuser
# 	resp = client.patch("/v1/users/admin@example.com", json=data, headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 404, 422)
# 	# As regular user
# 	resp = client.patch("/v1/users/admin@example.com", json=data, headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code == 403


# def test_delete_user_me(client, superuser_token, regular_token):
# 	# Not authenticated
# 	resp = client.delete("/v1/users/me")
# 	assert resp.status_code in (401, 403)
# 	# As superuser
# 	resp = client.delete("/v1/users/me", headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 404)
# 	# As regular user
# 	resp = client.delete("/v1/users/me", headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code in (200, 404)


# def test_delete_user(client, superuser_token, regular_token):
# 	# Not authenticated
# 	resp = client.delete("/v1/users/admin@example.com")
# 	assert resp.status_code in (401, 403, 404)
# 	# As superuser
# 	resp = client.delete("/v1/users/admin@example.com", headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 404)
# 	# As regular user
# 	resp = client.delete("/v1/users/admin@example.com", headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code == 403


# def test_update_password_me(client, superuser_token, regular_token):
# 	data = {
# 		"old_password": "adminpass",
# 		"new_password": "newpassword"
# 	}
# 	# Not authenticated
# 	resp = client.patch("/v1/users/me/password", json=data)
# 	assert resp.status_code in (401, 403, 422)
# 	# As superuser
# 	resp = client.patch("/v1/users/me/password", json=data, headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 422)
# 	# As regular user
# 	data["old_password"] = "userpass"
# 	resp = client.patch("/v1/users/me/password", json=data, headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code in (200, 422)


# def test_register_user(client, superuser_token, regular_token):
# 	data = {
# 		"first_name": "Signup",
# 		"last_name": "User",
# 		"email": "signupuser@example.com",
# 		"password": "signupassword"
# 	}
# 	# Not authenticated
# 	resp = client.post("/v1/users/signup", json=data)
# 	assert resp.status_code in (200, 201, 400, 422)
# 	# As superuser
# 	resp = client.post("/v1/users/signup", json=data, headers={"Authorization": f"Bearer {superuser_token}"})
# 	assert resp.status_code in (200, 201, 400, 422)
# 	# As regular user
# 	resp = client.post("/v1/users/signup", json=data, headers={"Authorization": f"Bearer {regular_token}"})
# 	assert resp.status_code in (200, 201, 400, 422)
