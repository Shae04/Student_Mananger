from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, declarative_base

def dataBaseMain():
    Base = declarative_base()  #Create the base class
    engine = create_engine('sqlite:///project.db', echo=False)  # create database file, and set echo to false(does not show database commands)
    Session = sessionmaker(bind=engine)
    session = Session()  #Creates a session object to initiate query in the db

    class User(Base):  # create table for User
        __tablename__ = 'user'
        name = Column(String(32), primary_key=True, nullable=False)  # columns
        password = Column(String(512))

    class Student(Base):  # create table for student
        __tablename__ = 'student'  # columns
        id = Column(String(9), primary_key=True, unique=True)
        name = Column(String(32), nullable=False)
        age = Column(Integer)
        gender = Column(String(1))
        major = Column(String(32))
        phone = Column(String(32))

    class Score(Base):  # create table for score
        __tablename__ = 'score'
        id = Column(String(9), primary_key=True, unique=True)  # columns
        name = Column(String(32), nullable=False)
        CS1030 = Column(Integer)
        CS1100 = Column(Integer)
        CS2030 = Column(Integer)

    Base.metadata.create_all(engine)

    return session, User, Student, Score
