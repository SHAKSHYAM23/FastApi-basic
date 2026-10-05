from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    # Used for POST bodies. Pydantic validates the incoming JSON before the
    # route runs; invalid data automatically produces a 422 response.
    title: str = Field(min_length=1, max_length=100)
    description: str = ""
    completed: bool = False
    topic: str | None = None


class TaskUpdate(BaseModel):
    # Used for PUT bodies. PUT replaces the whole task, so it has the
    # same fields as TaskCreate. A separate class makes it easy to
    # change one later without touching the other.
    title: str = Field(min_length=1, max_length=100)
    description: str = ""
    completed: bool = False
    topic: str | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    topic: str | None = None

    # Lets Pydantic read data from a SQLAlchemy object (task.title)
    # instead of only from a dict (task["title"]).
    model_config = ConfigDict(from_attributes=True)


class ExternalInfoResponse(BaseModel):
    task_id: int
    topic: str
    wikipedia_title: str
    snippet: str
    url: str