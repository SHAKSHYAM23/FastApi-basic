# FastAPI Task Manager + Wikipedia Info

A small learning project that connects FastAPI routes, Pydantic schemas, a service layer, SQLAlchemy, SQLite, and an external API call using `httpx`.

## Features

- Full CRUD for tasks, with pagination (`?page=1&limit=10`)
- Request and response validation with Pydantic
- Database sessions injected with `Depends(get_db)`
- `GET /tasks/{task_id}/external-info` looks up a task's topic on Wikipedia using `httpx.AsyncClient`
- Error handling with `HTTPException` (400, 404, 422, 502, 503, 504)
- Configuration loaded from `.env`

## Tech stack

FastAPI, SQLAlchemy, SQLite, Pydantic, pydantic-settings, httpx, Uvicorn

## Project structure

```text
app/
├── main.py              # creates the app, tables, and includes the router
├── config/settings.py   # reads .env into a typed settings object
├── database/connection.py   # engine, SessionLocal, Base, get_db()
├── models/task.py       # SQLAlchemy table definition
├── schemas/task.py      # Pydantic request/response models
├── services/task_service.py # database logic + external API call
└── routers/tasks.py     # HTTP endpoints
```

Request flow: `main → router → schema → service → database`, and for the external API: `router → service → httpx → Wikipedia`.

## Setup

Requires Python 3.10 or newer.

```bash
# 1. Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows
# source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate           # Windows CMD

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create your .env from the template
cp .env.example .env
# then put your own email in WIKI_USER_AGENT

# 4. Run the server (from the folder containing app/)
uvicorn app.main:app --reload
```

Open the interactive docs at http://127.0.0.1:8000/docs

The SQLite file `tasks.db` is created automatically on first run.

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/tasks` | Create a task |
| GET | `/tasks?page=1&limit=10` | List tasks (paginated) |
| GET | `/tasks/{task_id}` | Get one task |
| PUT | `/tasks/{task_id}` | Replace a task |
| DELETE | `/tasks/{task_id}` | Delete a task |
| GET | `/tasks/{task_id}/external-info` | Wikipedia summary for the task's topic |

## Status codes used

201 created, 204 deleted, 400 task has no topic, 404 not found, 422 validation error, 502 external API failed, 503 rate limited, 504 external API timeout.

## Example request

```json
POST /tasks
{
  "title": "Learn FastAPI",
  "description": "Finish the project",
  "topic": "FastAPI"
}
```