from sqlalchemy.ext.declarative import declarative_base
from databases import Database
from settings import SQLALCHEMY_DATABASE_URL

#  createuser sqlalchemy_user -P
#  createdb sqlalchemy_db -Osqlalchemy_user

db = Database(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
