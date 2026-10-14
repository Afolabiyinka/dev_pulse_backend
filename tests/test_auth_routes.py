from itertools import count
from types import SimpleNamespace
from urllib.parse import parse_qs, urlparse
from uuid import UUID
from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.app import app
from app.core.config import envVariables
from app.database.db_session import get_db
from app.modules.auth import auth_routes


_client_ips = count(1)
USER_ID = UUID("aa38a58c-f929-4b5c-bc00-8e81c4ea0156")


@pytest.fixture
def client():
    ip = f"198.51.100.{next(_client_ips)}"

    def override_get_db():
        yield None

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app, client=(ip, 50000)) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_signup_returns_success_and_sets_auth_cookie(client, monkeypatch):
    monkeypatch.setattr(
        auth_routes.auth_service,
        "register_user",
        lambda db, data: SimpleNamespace(id=USER_ID),
    )

    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "person@example.com", "password": "valid-pass-123"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Account created successfully"}
    assert "access_token=" in response.headers["set-cookie"]


def test_signup_rejects_invalid_request(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "not-an-email", "password": "short"},
    )

    assert response.status_code == 422


def test_signup_returns_bad_request_for_existing_email(client, monkeypatch):
    def reject_existing_email(db, data):
        raise ValueError("Email already in use")

    monkeypatch.setattr(
        auth_routes.auth_service,
        "register_user",
        reject_existing_email,
    )

    response = client.post(
        "/api/v1/auth/signup",
        json={"email": "person@example.com", "password": "valid-pass-123"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already in use"}


def test_login_returns_success_and_sets_auth_cookie(client, monkeypatch):
    monkeypatch.setattr(
        auth_routes.auth_service,
        "authenticate_user",
        lambda db, data: SimpleNamespace(id=USER_ID),
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "person@example.com", "password": "valid-pass-123"},
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Logged in"}
    assert "access_token=" in response.headers["set-cookie"]


def test_login_rejects_invalid_credentials(client, monkeypatch):
    monkeypatch.setattr(
        auth_routes.auth_service,
        "authenticate_user",
        lambda db, data: None,
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "person@example.com", "password": "valid-pass-123"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}


def test_login_is_rate_limited_after_five_attempts(client, monkeypatch):
    monkeypatch.setattr(
        auth_routes.auth_service,
        "authenticate_user",
        lambda db, data: None,
    )

    payload = {"email": "person@example.com", "password": "valid-pass-123"}
    responses = [
        client.post("/api/v1/auth/login", json=payload)
        for _ in range(6)
    ]

    assert [response.status_code for response in responses] == [
        401,
        401,
        401,
        401,
        401,
        429,
    ]


def test_global_rate_limit_applies_to_undecorated_routes(client):
    responses = [client.get("/openapi.json") for _ in range(101)]

    assert all(response.status_code == 200 for response in responses[:100])
    assert responses[-1].status_code == 429


def test_logout_clears_auth_cookie(client):
    response = client.post("/api/v1/auth/logout")

    assert response.status_code == 200
    assert response.json() == {"message": "Logged out"}
    assert "access_token=" in response.headers["set-cookie"]
    assert "Max-Age=0" in response.headers["set-cookie"]


def test_github_login_redirects_with_oauth_parameters(client):
    response = client.get("/api/v1/auth/github", follow_redirects=False)

    assert response.status_code == 307
    query = parse_qs(urlparse(response.headers["location"]).query)
    assert query["client_id"] == [envVariables.github_client_id]
    assert query["redirect_uri"] == [envVariables.github_redirect_uri]
    assert query["scope"] == ["read:user user:email repo"]


def test_github_callback_without_code_redirects_to_login(client):
    response = client.get("/api/v1/auth/github/callback", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == (
        f"{envVariables.frontend_url.rstrip('/')}/auth/login"
        "?error=github_auth_failed"
    )


def test_github_callback_success_redirects_and_sets_auth_cookie(
    client, monkeypatch
):
    monkeypatch.setattr(
        auth_routes.github_services,
        "exchange_github_code",
        AsyncMock(return_value="github-token"),
    )
    monkeypatch.setattr(
        auth_routes.auth_service,
        "authenticate_github_user",
        AsyncMock(return_value=SimpleNamespace(id=USER_ID)),
    )

    response = client.get(
        "/api/v1/auth/github/callback?code=github-code",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"] == envVariables.frontend_url
    assert "access_token=" in response.headers["set-cookie"]
