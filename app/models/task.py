from sqlalchemy import Boolean, Column, Integer, String

from app.database.connection import Base


class Task(Base):
    __tablename__ = "tasks"

    # primary_key=True: unique ID, auto-incremented by SQLite
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    completed = Column(Boolean, nullable=False, default=False)
    # Used by the external-info endpoint. nullable=True means it may be empty.
    topic = Column(String, nullable=True)