
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from app.modules.github import github_schemas
from app.modules.github import github_services
from app.modules.auth.auth_dependency import auth_middleware
from app.database import db_session
from app.core.rate_limiter import GLOBAL_RATE_LIMIT, limiter


GithubRouter = APIRouter(prefix="/github", tags=["GitHub"])


@GithubRouter.get(
    "/repos",
    response_model=github_schemas.GitHubRepositoriesResponse,
)
@limiter.limit(GLOBAL_RATE_LIMIT)
async def list_github_repositories(
    request: Request,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    current_user_id=Depends(auth_middleware),
    db: Session = Depends(db_session.get_db),

):
    return await github_services.get_github_repositories(
        user_id=current_user_id,
        page=page,
        per_page=per_page,
        db=db
    )
