
from datetime import datetime
from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    HttpUrl,
    field_validator,
)


class GitHubOwner(BaseModel):
    model_config = ConfigDict(extra="ignore")

    login: str
    id: int
    node_id: str
    avatar_url: HttpUrl
    gravatar_id: str
    url: HttpUrl
    html_url: HttpUrl
    followers_url: HttpUrl
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: HttpUrl
    organizations_url: HttpUrl
    repos_url: HttpUrl
    events_url: str
    received_events_url: HttpUrl
    type: str
    user_view_type: str
    site_admin: bool


class GitHubRepository(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    owner: GitHubOwner
    html_url: HttpUrl
    description: str | None = None
    fork: bool
    url: HttpUrl

    forks_url: HttpUrl
    keys_url: str
    collaborators_url: str
    teams_url: HttpUrl
    hooks_url: HttpUrl
    issue_events_url: str
    events_url: HttpUrl
    assignees_url: str
    branches_url: str
    tags_url: HttpUrl
    blobs_url: str
    git_tags_url: str
    git_refs_url: str
    trees_url: str
    statuses_url: str
    languages_url: HttpUrl
    stargazers_url: HttpUrl
    contributors_url: HttpUrl
    subscribers_url: HttpUrl
    subscription_url: HttpUrl
    commits_url: str
    git_commits_url: str
    comments_url: str
    issue_comment_url: str
    contents_url: str
    compare_url: str
    merges_url: HttpUrl
    archive_url: str
    downloads_url: HttpUrl
    issues_url: str
    pulls_url: HttpUrl
    milestones_url: str
    notifications_url: str
    labels_url: str
    releases_url: str
    deployments_url: HttpUrl

    created_at: datetime
    updated_at: datetime
    pushed_at: datetime | None = None

    git_url: str
    ssh_url: str
    clone_url: HttpUrl
    svn_url: HttpUrl
    homepage: HttpUrl | None = None

    @field_validator("homepage", mode="before")
    @classmethod
    def normalize_homepage(cls, value: Any) -> Any:
        if value == "":
            return None
        return value

    size: int
    stargazers_count: int
    watchers_count: int
    language: str | None = None

    has_issues: bool
    has_projects: bool
    has_downloads: bool
    has_wiki: bool
    has_pages: bool
    has_discussions: bool

    forks_count: int
    mirror_url: HttpUrl | None = None
    archived: bool
    disabled: bool
    open_issues_count: int
    license: dict[str, Any] | None = None

    allow_forking: bool
    is_template: bool
    web_commit_signoff_required: bool
    has_pull_requests: bool
    pull_request_creation_policy: str

    topics: list[str]
    visibility: str
    forks: int
    open_issues: int
    watchers: int
    default_branch: str

    permissions: dict[str, bool] | None = None


class GitHubRepositoriesResponse(BaseModel):
    repositories: list[GitHubRepository]
    page: int
    per_page: int
    has_more: bool
