import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def get_env_db_url():
    return os.getenv("DATABASE_URL")


def create_engine_from_env(**kwargs):
    return create_engine(get_env_db_url(), future=True, **kwargs)


def session_factory(**kwargs):
    engine = create_engine_from_env(**kwargs)
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    SessionLocal = session_factory()
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()
