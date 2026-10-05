from .app import app
from app.core.config import envVariables

__all__ = ["app", "main"]


# port = settings.

def main() -> None:
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=envVariables.port, reload=True)
