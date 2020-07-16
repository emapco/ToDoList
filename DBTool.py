from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

db_file_name = 'todo.db'
table_name = 'task'

Base = declarative_base()


class Table(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default-value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


def create_engine_session():
    # create db file and Base class to pass thru Table class.
    engine = create_engine('sqlite:///{0}?check_same_thread=False' .format(db_file_name))
    declarative_base().metadata.create_all(engine)  # create db based on engine db file

    Table.__table__.create(bind=engine, checkfirst=True)

    Session = sessionmaker(bind=engine)  # create db session based on engine connection source

    return Session()

