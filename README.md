# FastAPI Backend

Backend service built with FastAPI, SQLAlchemy, Pydantic Settings, and PostgreSQL.

## Requirements

- Python 3.13 or newer
- `uv`
- PostgreSQL database

## Setup

Install the project and development dependencies:

```powershell
uv sync
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your own JWT secret and database connection string. Do not commit `.env` because it contains secrets.

## Commands

Start the development server with reload enabled:

```powershell
uv run dev
```

Run the test suite:

```powershell
uv run test
```

Build source and wheel distributions:

```powershell
uv run build
```

The server listens on `http://localhost:8000` by default. Change `PORT` in `.env` to use another port.

## Endpoints

- `POST /auth/register` registers a user.

Interactive API documentation is available at `/docs` while the server is running.
