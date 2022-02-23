from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#  createuser sqlalchemy_user -P
#  createdb sqlalchemy_db -Osqlalchemy_user
SQLALCHEMY_DATABASE_URL = "postgresql://sqlalchemy_user:sqlpwd@localhost:5432/sqlalchemy_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
