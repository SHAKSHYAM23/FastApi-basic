from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config.settings import settings

# The engine is the actual connection "factory" to the database.
# check_same_thread=False is SQLite-specific: FastAPI may use different
# threads for the same request, and SQLite blocks that by default.
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
)

# SessionLocal is a class; calling SessionLocal() gives you a new session.
# A session is your "conversation" with the database: you add/query objects,
# then commit to save them.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Every model class inherits from Base, so SQLAlchemy knows which
# classes map to tables.
Base = declarative_base()


def get_db():
    # This is a dependency. FastAPI calls it for each request that asks for it
    # via Depends(get_db), and passes the yielded session into the route.
    db = SessionLocal()
    try:
        yield db  # the route runs while we're paused here
    finally:
        db.close()  # always runs afterwards, even if the route raised an error