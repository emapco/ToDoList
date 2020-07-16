from datetime import datetime, timedelta
import DBTool as db


def print_tasks(rows, is_date_visible, is_desc_visible):
    task_exist = False

    if (not is_date_visible) and is_desc_visible:
        for i in range(0, len(rows)):
            print('{0}. {1}'.format(i + 1, rows[i].task))
            task_exist = True

    if is_date_visible and is_desc_visible:
        for i in range(0, len(rows)):
            print('{0}. {1}. {2}'.format(i + 1, rows[i].task, datetime.strftime(rows[i].deadline, '%d %b')))
            task_exist = True

    if not task_exist:
        print("Nothing to do!")

    print()
    pass


def print_menu():
    print('1) Today\'s tasks\n'
          '2) Week\'s tasks\n'
          '3) All tasks\n'
          '4) Missed tasks\n'
          '5) Add task\n'
          '6) Delete task\n'
          '0) Exit \n')
    pass


session = db.create_engine_session()  # create db session

today = datetime.today()
option = 9  # set to (not zero) so program runs indefinitely until user enters appropriate value
while option != 0:

    print_menu()
    option = int(input())
    print()

    # print all task due today if none notifies user
    if option == 1:
        ui_rows = session.query(db.Table).filter(db.Table.deadline == today.date()).all()  # get rows with today's date

        print("Today {} :".format(datetime.strftime(today, '%d %b')))
        print_tasks(ui_rows, False, True)  # rows, is date visible, is desc visible

    # print all tasks due in the next week ([0,7] days)
    elif option == 2:
        next_week_date = today + timedelta(days=7)

        ui_rows = session.query(db.Table).filter(db.Table.deadline.between(today.date(), next_week_date.date())).all()

        print("{}:".format(datetime.strftime(next_week_date, '%A %d %b')))
        print_tasks(ui_rows, True, True)  # rows, is date visible, is desc visible

    # print all tasks saved
    elif option == 3:
        ui_rows = session.query(db.Table).all()  # get all rows from table

        print("All tasks:")
        print_tasks(ui_rows, True, True)  # rows, is date visible, is desc visible

    # print all tasks past the deadline
    elif option == 4:
        ui_rows = session.query(db.Table).filter(db.Table.deadline < today.date()).all()

        print("Missed tasks:")
        print_tasks(ui_rows, True, True)  # rows, is date visible, is desc visible

    # asks users for task description and deadline and adds&commits to database
    elif option == 5:
        new_task = input("Enter task:")
        new_deadline = datetime.strptime(input("Enter deadline (YYYY-MM-DD) :"), '%Y-%m-%d')
        new_row = db.Table(task=new_task, deadline=new_deadline)

        print('The task has been added!\n')

        session.add(new_row)
        session.commit()
    # asks users for tasks to be deleted and deletes&commits to database
    elif option == 6:
        ui_rows = session.query(db.Table).order_by(db.Table.deadline).all()  # get all rows from table ordered by date

        print('Chose the number of the task you want to delete:')
        print_tasks(ui_rows, True, True)  # rows, is date visible, is desc visible

        # get row index (1-based) and then delete from table (0-based)
        deleted_row_index = int(input())
        session.delete(ui_rows[deleted_row_index - 1])
        session.commit()

    # termination condition
    elif option == 0:
        print('Bye!')
