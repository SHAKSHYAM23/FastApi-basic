from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models import task as task_model  # noqa: F401  (registers Task with Base)
from app.routers import tasks

# Creates the tables that don't exist yet. It only knows about models that
# were imported above, which is why the models import is there.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager + Wikipedia Info")

# Attach all of the router's routes to the main app
app.include_router(tasks.router)