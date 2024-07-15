from sqlalchemy import Integer, Column, create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

class Person(Base):
    __tablename__ = "person"
    id = Column(String(50), primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)

uri = "sqlite:///person.db"
engine = create_engine(uri)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

# Create a configured "Session" class
session_factory = sessionmaker(bind=engine)
# Create a scoped session
Session = scoped_session(session_factory)
