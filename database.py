import sqlite3
from datetime import datetime
import sqlalchemy
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Sequence,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

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


def get_all_tasks(order_by_due_date: bool = False):
    session = get_session()
    try:
        query = session.query(Task)
        if order_by_due_date:
            query = query.order_by(Task.due_date)
        return query.all()
    finally:
        session.close()


def get_task_by_id(task_id: int) -> Task | None:
    session = get_session()
    try:
        return session.query(Task).filter(Task.id == task_id).first()
    finally:
        session.close()


def get_tasks_by_course(course: str):
    session = get_session()
    try:
        return session.query(Task).filter(Task.course == course).all()
    finally:
        session.close()


def update_task(task_id: int, **fields) -> Task | None:
    session = get_session()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None

        for key, value in fields.items():
            if hasattr(task, key):
                setattr(task, key, value)

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
