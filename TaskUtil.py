from datetime import datetime, timedelta

import DBTool as db

today = datetime.today()


# generate list with task index, description, and deadline date
def get_list(rows):
    task_list = []

    for i in range(0, len(rows)):
        task_list.append([i, rows[i].task, rows[i].deadline])

    return task_list, rows


# gets tasks based on option specified
def get_tasks(session, option):
    # gets task due today
    if option == 1:
        # get rows (query result) with today's date
        rows = session.query(db.Table).filter(db.Table.deadline == today.date()).all()
        return get_list(rows)

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
def delete_task(session, rows, index):
    print(index)
    session.delete(rows[index])
    session.commit()
