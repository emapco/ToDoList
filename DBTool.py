from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from Task import Task

DB_FILE_NAME = 'todo.db'
TABLE_NAME = 'task'
BASE = declarative_base()

TODAY = datetime.today()
NEXT_WEEK_DATE = TODAY + timedelta(days=7)

TODAY_TASK_OPTION = 1
WEEK_TASK_OPTION = 2
ALL_TASK_OPTION = 3
MISSED_TASK_OPTION = 4

SUCCESS = True
ERROR = False


class Table(BASE):
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default-value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class TaskDatabase:
    def __init__(self):
        self.session = self._create_engine_session()
        self.Table = Table

    """
    ##########################################################################
                                Public Functions
    ##########################################################################
    """
    def get_tasks(self, option: int) -> list:
        """Queries the database with appropriate SELECT statement
        depending on user inputted option.

        Arguments:
        option -- type of request
        """
        if option == TODAY_TASK_OPTION:  # gets task due today
            rows = self.session.query(self.Table).filter(self.Table.deadline == TODAY.date()).all()
        elif option == WEEK_TASK_OPTION:  # gets tasks due in the next week ([0,7] days)
            rows = self.session.query(self.Table).filter(self.Table.deadline.between(TODAY.date(), NEXT_WEEK_DATE.date())).all()
        elif option == ALL_TASK_OPTION:  # gets all tasks saved
            rows = self.session.query(self.Table).all()  # get all rows from table
        else:  # option == MISSED_TASK_OPTION; gets all tasks past the deadline
            rows = self.session.query(self.Table).filter(self.Table.deadline < TODAY.date()).all()
        return rows

    def add_task(self, task: Task) -> bool:
        """Saves user inputted task to database

        Arguments:
        task -- task object to be added to database
        """
        try:
            desc = task.desc.get()
            date = datetime.strptime(task.date.get(), '%Y-%m-%d')

            new_row = self.Table(task=desc, deadline=date)

            self.session.add(new_row)
            self.session.commit()

            return SUCCESS
        except ValueError:
            return ERROR

    def delete_task(self, rows: list, index: int) -> bool:
        """Deletes task based on which delete button was pressed

        Arguments:
        rows -- database query results
        index -- index of task to be deleted
        """
        try:
            self.session.delete(rows[index])
            self.session.commit()

            return SUCCESS
        except IndexError:
            return ERROR

    """
    ##########################################################################
                                Static Functions
    ##########################################################################
    """
    @staticmethod
    def _create_engine_session():
        """
        Private static function used to create/initiate database session.
        """
        # create db file and Base class to pass thru Table class.
        engine = create_engine('sqlite:///{0}?check_same_thread=False'.format(DB_FILE_NAME))
        declarative_base().metadata.create_all(engine)  # create db based on engine db file

        Table.__table__.create(bind=engine, checkfirst=True)  # checks if table exists, if not creates it; crashes otherwise

        Session = sessionmaker(bind=engine)  # create db session based on engine connection source

        return Session()





