from main import *

import sqlalchemy
import sqlite3

from sqlalchemy import create_engine, Column, Float, Integer, String, ForeignKey, Table, Sequence, func
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.orm import joinedload

engine = create_engine('sqlite:///tasks.db')