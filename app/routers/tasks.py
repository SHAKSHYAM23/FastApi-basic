from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.task import (
    ExternalInfoResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)
from app.services import task_service

# prefix means every route below starts with /tasks
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db)):
    # task_in: FastAPI reads the JSON body, validates it against TaskCreate,
    #          and only then calls this function.
    # db: Depends(get_db) makes FastAPI call get_db() and pass in the session.
    # response_model: whatever we return is converted to TaskResponse JSON.
    return task_service.create_task(db, task_in)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    # Query parameters: /tasks?page=2&limit=5
    # ge/le add validation (ge = greater or equal, le = less or equal)
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return task_service.get_tasks(db, page, limit)


@router.get("/{task_id}", response_model=TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    # task_id is a path parameter: it matches {task_id} in the URL,
    # and the `int` type hint makes FastAPI validate and convert it.
    return task_service.get_task(db, task_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db)):
    # Path parameter + request body + dependency, all in one route
    return task_service.update_task(db, task_id, task_in)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    # 204 No Content: success, and there is no response body to send
    task_service.delete_task(db, task_id)


@router.get("/{task_id}/external-info", response_model=ExternalInfoResponse)
async def task_external_info(task_id: int, db: Session = Depends(get_db)):
    # async def here because we `await` the service call.
    # The other routes use plain `def`: FastAPI runs those in a thread pool,
    # which is the right choice for blocking (sync) database code.
    return await task_service.get_external_info(db, task_id)