from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# PostgreSQL / MySQL 需要不同的连接参数
if settings.is_postgres:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
    )
elif settings.is_mysql:
    engine = create_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        pool_recycle=3600,
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
