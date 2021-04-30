from datetime import datetime, timedelta

import DBTool as db

SUCCESS = 1
ERROR = -1
today = datetime.today()
next_week_date = today + timedelta(days=7)


def get_tasks(session, option):
    """Queries the database with appropriate SELECT statement
    depending on user inputted option.

    Arguments:
    session -- database session object
    option -- type of request
    """
    if option == 1:  # gets task due today
        rows = session.query(db.Table).filter(db.Table.deadline == today.date()).all()
    elif option == 2:  # gets tasks due in the next week ([0,7] days)
        rows = session.query(db.Table).filter(db.Table.deadline.between(today.date(), next_week_date.date())).all()
    elif option == 3:  # gets all tasks saved
        rows = session.query(db.Table).all()  # get all rows from table
    else:  # option == 4; gets all tasks past the deadline
        rows = session.query(db.Table).filter(db.Table.deadline < today.date()).all()

    return rows


def add_task(session, task):
    """Saves user inputted task to database

    Arguments:
    session -- database session object
    task -- task object to be added to database
    """
    try:
        desc = task.desc.get()
        date = datetime.strptime(task.date.get(), '%Y-%m-%d')

        new_row = db.Table(task=desc, deadline=date)

        session.add(new_row)
        session.commit()

        return SUCCESS
    except ValueError:
        return ERROR


def delete_task(session, rows, index):
    """Deletes task based on which delete button was pressed

    Arguments:
    session -- database session object
    rows -- database query results
    index -- index of task to be deleted
    """
    try:
        session.delete(rows[index])
        session.commit()

        return SUCCESS
    except IndexError:
        return ERROR
