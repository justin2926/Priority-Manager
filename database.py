import sqlalchemy
import sqlite3

from sqlalchemy import create_engine, Column, Float, Integer, String, ForeignKey, Table, Sequence, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm import joinedload

engine = create_engine("sqlite:///tasks.db", echo=False, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        Integer,
        Sequence("task_id", start=1, increment=1),
        primary_key=True
    )
    course = Column(String, nullable=False)
    assignment = Column(String, nullable=False)
    due_date = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    status = Column(String, default="pending")

    def __repr__(self):
        return (
            f"Task(id={self.id}, course={self.course!r}, "
            f"assignment={self.assignment!r}, due_date={self.due_date!r}, "
            f"priority={self.priority!r}, status={self.status!r})"
        )


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
print("Database and tables created successfully")

def get_session():
    return SessionLocal()

def add_task(course: str, assignment: str, due_date: str,
             priority: str, status: str = "pending") -> Task:
    session = get_session()
    try:
        task = Task(
            course=course,
            assignment=assignment,
            due_date=due_date,
            priority=priority,
            status=status,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    finally:
        session.close()

def delete_task(task_id: int) -> bool:
    session = get_session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False

        session.delete(task)
        session.commit()
        return True
    finally:
        session.close()

def change_status(task_id: int) -> bool:
    session = get_session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False

        task.status = 'completed'
        session.commit()
        return True
    finally:
        session.close()
