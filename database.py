import sqlalchemy
import sqlite3

from sqlalchemy import create_engine, Column, Float, Integer, String, ForeignKey, Table, Sequence, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm import joinedload

engine = create_engine('sqlite:///tasks.db')

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, Sequence('task_id', start=0, increment=1), primary_key=True)
    course = Column(String)
    assignment = Column(String)
    due_date = Column(String)
    priority = Column(String)

    def __rep__(self):
        return f"Task(id={self.id}, course={self.course}, assignment={self.assignment}, due_date={self.due_date}, priority={self.due_date})"
    
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

print("Database and tables created successfully")

