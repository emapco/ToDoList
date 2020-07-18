from datetime import datetime, timedelta

import DBTool as db

today = datetime.today()


# generate list with task index, description, and deadline date
def get_list(rows):
    task_list = []

    for i in range(0, len(rows)):
        task_list.append([i, rows[i].task, rows[i].deadline])

    return task_list


# gets tasks based on option specified
def get_tasks(session, option):
    # gets task due today if none notifies user
    if option == 1:
        rows = session.query(db.Table).filter(db.Table.deadline == today.date()).all()  # get rows with today's date
        return get_list(rows)  # rows, is date visible, is desc visible

    # gets tasks due in the next week ([0,7] days)
    elif option == 2:
        next_week_date = today + timedelta(days=7)

        rows = session.query(db.Table).filter(db.Table.deadline.between(today.date(), next_week_date.date())).all()
        return get_list(rows)

    # gets all tasks saved
    elif option == 3:
        rows = session.query(db.Table).all()  # get all rows from table
        return get_list(rows)

    # gets all tasks past the deadline
    elif option == 4:
        rows = session.query(db.Table).filter(db.Table.deadline < today.date()).all()
        return get_list(rows)


# Add task and commits to db
def add_task(session, task_desc, task_date):
    new_row = db.Table(task=task_desc, deadline=task_date)

    session.add(new_row)
    session.commit()


# Delete task and commits to db
def delete_task(session, index):
    rows = session.query(db.Table).order_by(db.Table.deadline).all()  # get all rows from table ordered by date

    # get row index (1-based) and then delete from table (0-based)
    session.delete(rows[int(index)])
    session.commit()
