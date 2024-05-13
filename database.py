import os

import databases
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL",
                                                 "postgresql+asyncpg://postgres:password@localhost/postgres")
        self.database = databases.Database(self.SQLALCHEMY_DATABASE_URL)

        self.engine = create_async_engine(self.SQLALCHEMY_DATABASE_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
