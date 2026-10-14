from types import SimpleNamespace
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.app import app
from app.core.token_helper import create_token
from app.database.db_session import get_db
from app.modules.account import account_routes

USER_ID = UUID("aa38a58c-f929-4b5c-bc00-8e81c4ea0156")


@pytest.fixture
def client():
    def override_get_db():
        yield None

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def auth_cookies(user_id: UUID = USER_ID):
    return {"access_token": create_token({"userid": str(user_id)})}


def test_get_account_me_returns_user(client, monkeypatch):
    user = SimpleNamespace(
        id=USER_ID,
        email="person@example.com",
        avatar="https://example.com/avatar.png",
        github_username="octocat",
        github_name="Octocat",
        github_authenticated=True,
    )
    monkeypatch.setattr(account_routes, "get_user_by_id", lambda db, user_id: user)

    response = client.get("/api/v1/account/me", cookies=auth_cookies())

    assert response.status_code == 200
    assert response.json() == {
        "id": str(USER_ID),
        "email": "person@example.com",
        "avatar": "https://example.com/avatar.png",
        "github_username": "octocat",
        "github_name": "Octocat",
        "github_authenticated": True,
    }


def test_get_account_me_requires_auth(client):
    response = client.get("/api/v1/account/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_get_account_me_returns_not_found_for_missing_user(client, monkeypatch):
    monkeypatch.setattr(account_routes, "get_user_by_id", lambda db, user_id: None)

    response = client.get("/api/v1/account/me", cookies=auth_cookies())

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_edit_account_me_updates_profile(client, monkeypatch):
    user = SimpleNamespace(
        id=USER_ID,
        email="person@example.com",
        avatar="https://example.com/old-avatar.png",
        github_username="old-user",
        github_name="Old Name",
        github_authenticated=False,
    )
    monkeypatch.setattr(account_routes, "get_user_by_id", lambda db, user_id: user)

    def fake_update_account(db, user, data):
        return SimpleNamespace(
            id=user.id,
            email=user.email,
            avatar=data.avatar,
            github_username=data.github_username,
            github_name=data.github_name,
            github_authenticated=user.github_authenticated,
        )

    monkeypatch.setattr(account_routes.account_service, "update_account", fake_update_account)

    response = client.patch(
        "/api/v1/account/me",
        json={"avatar": "https://example.com/new-avatar.png", "github_name": "New Name"},
        cookies=auth_cookies(),
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": str(USER_ID),
        "email": "person@example.com",
        "avatar": "https://example.com/new-avatar.png",
        "github_username": None,
        "github_name": "New Name",
        "github_authenticated": False,
    }


def test_delete_account_me_removes_user(client, monkeypatch):
    user = SimpleNamespace(id=USER_ID)
    monkeypatch.setattr(account_routes, "get_user_by_id", lambda db, user_id: user)
    monkeypatch.setattr(account_routes.account_service, "delete_account", lambda db, user: None)

    response = client.delete("/api/v1/account/me", cookies=auth_cookies())

    assert response.status_code == 204
    assert response.content == b""
