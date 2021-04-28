from datetime import datetime, timedelta

import DBTool as db
from Task import Task

today = datetime.today()


# generate list with task index, description, and deadline date
def get_list(rows):
    task_dict = {}

    for i in range(0, len(rows)):
        task_dict[i] = Task(rows[i].task, rows[i].deadline)

    return task_dict, rows


# gets tasks based on option specified
def get_tasks(session, option):
    if option == 1:  # gets task due today
        rows = session.query(db.Table).filter(db.Table.deadline == today.date()).all()
        return get_list(rows)
    elif option == 2:  # gets tasks due in the next week ([0,7] days)
        next_week_date = today + timedelta(days=7)
        rows = session.query(db.Table).filter(db.Table.deadline.between(today.date(), next_week_date.date())).all()
        return get_list(rows)
    elif option == 3:  # gets all tasks saved
        rows = session.query(db.Table).all()  # get all rows from table
        return get_list(rows)
    else:  # option == 4; gets all tasks past the deadline
        rows = session.query(db.Table).filter(db.Table.deadline < today.date()).all()
        return get_list(rows)


# Add task and commits to db
def add_task(session, task):
    try:
        desc = task.desc.get()
        date = datetime.strptime(task.date.get(), '%Y-%m-%d')

        new_row = db.Table(task=desc, deadline=date)

        session.add(new_row)
        session.commit()

        # add popup confirmation screen and set fields to '' after adding
    except ValueError:
        # add popup error screen (for date formatting issues)
        pass


# Delete task and commits to db
def delete_task(session, rows, index):
    try:
        session.delete(rows[index])
        session.commit()
    except IndexError:
        print('No task')

        # TODO: add popup for invalid task as well as when task is properly deleted
