from .app import app
from .config import settings

__all__ = ["app", "main"]


# port = settings.

def main() -> None:
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=settings.port, reload=True)
