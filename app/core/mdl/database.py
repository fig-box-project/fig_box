from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# TODO 全部解耦后尝试将hasidmdl指向这里

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency, 从路由获取数据库操作权时要调用这个
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
