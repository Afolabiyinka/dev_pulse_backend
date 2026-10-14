from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.app import app
from app.core.token_helper import create_token
from app.database.db_session import get_db
from app.modules.github import github_routes

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


def build_repository_payload(name: str, full_name: str):
    return {
        "id": 1,
        "node_id": "MDEwOlJlcG9zaXRvcnkx",
        "name": name,
        "full_name": full_name,
        "private": False,
        "owner": {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://avatars.githubusercontent.com/u/1?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "user_view_type": "standard",
            "site_admin": False,
        },
        "html_url": "https://github.com/octocat/sample-repo",
        "description": "Example repository",
        "fork": False,
        "url": "https://api.github.com/repos/octocat/sample-repo",
        "forks_url": "https://api.github.com/repos/octocat/sample-repo/forks",
        "keys_url": "https://api.github.com/repos/octocat/sample-repo/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/octocat/sample-repo/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/octocat/sample-repo/teams",
        "hooks_url": "https://api.github.com/repos/octocat/sample-repo/hooks",
        "issue_events_url": "https://api.github.com/repos/octocat/sample-repo/issues/events{/number}",
        "events_url": "https://api.github.com/repos/octocat/sample-repo/events",
        "assignees_url": "https://api.github.com/repos/octocat/sample-repo/assignees{/user}",
        "branches_url": "https://api.github.com/repos/octocat/sample-repo/branches{/branch}",
        "tags_url": "https://api.github.com/repos/octocat/sample-repo/tags",
        "blobs_url": "https://api.github.com/repos/octocat/sample-repo/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/octocat/sample-repo/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/octocat/sample-repo/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/octocat/sample-repo/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/octocat/sample-repo/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/octocat/sample-repo/languages",
        "stargazers_url": "https://api.github.com/repos/octocat/sample-repo/stargazers",
        "contributors_url": "https://api.github.com/repos/octocat/sample-repo/contributors",
        "subscribers_url": "https://api.github.com/repos/octocat/sample-repo/subscribers",
        "subscription_url": "https://api.github.com/repos/octocat/sample-repo/subscription",
        "commits_url": "https://api.github.com/repos/octocat/sample-repo/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/octocat/sample-repo/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/octocat/sample-repo/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/octocat/sample-repo/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/octocat/sample-repo/contents/{+path}",
        "compare_url": "https://api.github.com/repos/octocat/sample-repo/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/octocat/sample-repo/merges",
        "archive_url": "https://api.github.com/repos/octocat/sample-repo/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/octocat/sample-repo/downloads",
        "issues_url": "https://api.github.com/repos/octocat/sample-repo/issues{/number}",
        "pulls_url": "https://api.github.com/repos/octocat/sample-repo/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/octocat/sample-repo/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/octocat/sample-repo/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/octocat/sample-repo/labels{/name}",
        "releases_url": "https://api.github.com/repos/octocat/sample-repo/releases{/id}",
        "deployments_url": "https://api.github.com/repos/octocat/sample-repo/deployments",
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-10T00:00:00Z",
        "pushed_at": "2024-01-09T00:00:00Z",
        "git_url": "git://github.com/octocat/sample-repo.git",
        "ssh_url": "git@github.com:octocat/sample-repo.git",
        "clone_url": "https://github.com/octocat/sample-repo.git",
        "svn_url": "https://github.com/octocat/sample-repo",
        "homepage": None,
        "size": 120,
        "stargazers_count": 12,
        "watchers_count": 7,
        "language": "Python",
        "has_issues": True,
        "has_projects": True,
        "has_downloads": True,
        "has_wiki": True,
        "has_pages": False,
        "has_discussions": False,
        "forks_count": 3,
        "mirror_url": None,
        "archived": False,
        "disabled": False,
        "open_issues_count": 2,
        "license": None,
        "allow_forking": True,
        "is_template": False,
        "web_commit_signoff_required": False,
        "has_pull_requests": True,
        "pull_request_creation_policy": "all",
        "topics": ["python", "api"],
        "visibility": "public",
        "forks": 3,
        "open_issues": 2,
        "watchers": 7,
        "default_branch": "main",
        "permissions": {"admin": True, "maintain": True, "push": True, "triage": False, "pull": True},
    }


def test_list_github_repositories_returns_results(client, monkeypatch):
    async def fake_get_github_repositories(user_id, page, per_page, db):
        assert user_id == USER_ID
        assert page == 2
        assert per_page == 5
        return {
            "repositories": [
                build_repository_payload("sample-repo", "octocat/sample-repo"),
                build_repository_payload("another-repo", "octocat/another-repo"),
            ],
            "page": 2,
            "per_page": 5,
            "has_more": False,
        }

    monkeypatch.setattr(github_routes.github_services, "get_github_repositories", fake_get_github_repositories)

    response = client.get(
        "/api/v1/github/repos?page=2&per_page=5",
        cookies=auth_cookies(),
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 2
    assert payload["per_page"] == 5
    assert payload["has_more"] is False
    assert len(payload["repositories"]) == 2
    assert payload["repositories"][0]["name"] == "sample-repo"
    assert payload["repositories"][0]["full_name"] == "octocat/sample-repo"
    assert payload["repositories"][1]["name"] == "another-repo"
    assert payload["repositories"][1]["full_name"] == "octocat/another-repo"


def test_list_github_repositories_requires_auth(client):
    response = client.get("/api/v1/github/repos")

    assert response.status_code == 401
    assert response.json() == {"detail": "Authentication required"}


def test_list_github_repositories_surfaces_service_error(client, monkeypatch):
    async def fake_get_github_repositories(user_id, page, per_page, db):
        raise HTTPException(status_code=400, detail="GitHub account is not connected")

    monkeypatch.setattr(github_routes.github_services, "get_github_repositories", fake_get_github_repositories)

    response = client.get("/api/v1/github/repos", cookies=auth_cookies())

    assert response.status_code == 400
    assert response.json() == {"detail": "GitHub account is not connected"}
