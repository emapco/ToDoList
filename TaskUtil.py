from datetime import datetime, timedelta

import DBTool as db

today = datetime.today()
next_week_date = today + timedelta(days=7)


# gets tasks based on option specified
def get_tasks(session, option):
    """Queries the database with appropriate SELECT statement
    depending on user inputted option.

    Keyword arguments:
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


# Add task and commits to db
def add_task(session, task):
    """Saves user inputted task to database

    Keyword arguments:
    session -- database session object
    task -- task object to be added to database
    """
    try:
        desc = task.desc.get()
        date = datetime.strptime(task.date.get(), '%Y-%m-%d')

        new_row = db.Table(task=desc, deadline=date)

        session.add(new_row)
        session.commit()

    except ValueError:
        print("Error with new task")
        pass


# Delete task and commits to db
def delete_task(session, rows, index):
    try:
        session.delete(rows[index])
        session.commit()
    except IndexError:
        print('No task')
