from datetime import datetime

from tkinter import *
from tkinter import ttk

from DBTool import create_engine_session
import TaskUtil as tu


# logic for menu buttons
def display_today_tasks(*args):
    tasks = tu.get_tasks(session, option=1)  # list [[index, task desc str, task date str],[]]
    update_ui_task(tasks, ui_rows)
    pass


def display__week_tasks(*args):
    tasks = tu.get_tasks(session, option=2)  # list [[index, task desc str, task date str],[]]
    update_ui_task(tasks, ui_rows)
    pass


def display_all_tasks(*args):
    tasks = tu.get_tasks(session, option=3)  # list [[index, task desc str, task date str],[]]
    update_ui_task(tasks, ui_rows)
    pass


def display_missed_tasks(*args):
    tasks = tu.get_tasks(session, option=4)  # list [[index, task desc str, task date str],[]]
    update_ui_task(tasks, ui_rows)
    pass


# logic for displaying next set of tasks
def update_ui_task(tasks, ui_rows):
    for current_row in range(2, ui_rows):
        try:
            # catch indexerror in case empty query is returned
            task_index = StringVar().set(tasks[current_row-1][0])
            task_desc = StringVar().set(tasks[current_row-1][1])
            task_date = StringVar().set(tasks[current_row-1][2].isoformat())  # converts datetime.date to str MMMM-MM-DD

            print("current index:row, desc, date: {}:{}, {}, {}" .format(current_row-1, current_row,
                                                                         tasks[current_row][1],
                                                                         tasks[current_row][2].isoformat()))

            ttk.Label(mainframe, textvariable=task_desc).grid(column=2, row=current_row)
            ttk.Label(mainframe, textvariable=task_date).grid(column=3, row=current_row)
            ttk.Button(mainframe, text="Del", command=delete_task).grid(column=4, row=current_row,
                                                                                             sticky=E)
        except IndexError:
            pass
    pass


# logic for add task button
def add_task(*args):
    try:
        task_desc = new_task_desc.get()
        task_date = datetime.strptime(new_task_date.get(), '%Y-%m-%d')

        #print(task_desc)
        #print(task_date)

        tu.add_task(session, task_desc, task_date)

        #add popup confirmation screen here
    except ValueError:
        pass
    pass


# logic for del tasks button
def delete_task(*args):
    #TU.delete_task(session, index)
    pass


session = create_engine_session()  # create db session
ui_columns = 4
ui_rows = 10

root = Tk()
root.title('To Do List')

mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(ui_columns, ui_rows))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.geometry("575x500+300+300")  # window width x window height + position right + position down

task_desc = StringVar()
task_date = StringVar()
new_task_desc = StringVar()
new_task_date = StringVar()

# Displayed tasks: menu and instances
ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=NW)
ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=NW)
ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=N)


# print task's desc and deadline for selected range (task = [[desc., deadline],[desc., deadline],...]
for current_row in range(2, ui_rows):
    ttk.Label(mainframe, textvariable=task_desc).grid(column=2, row=current_row)
    ttk.Label(mainframe, textvariable=task_date).grid(column=3, row=current_row)
    ttk.Button(mainframe, text="Del", command=delete_task).grid(column=4, row=current_row, sticky=E)

# Task menu button elements
ttk.Label(mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Today\'s tasks", command=display_today_tasks).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Week\'s tasks", command=display__week_tasks).grid(column=1, row=3, sticky=W)
ttk.Button(mainframe, text="All tasks", command=display_all_tasks).grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Missed tasks", command=display_missed_tasks).grid(column=1, row=5, sticky=W)

# Add new task GUI elements (to the last row)
ttk.Label(mainframe, text="Add task description \nand deadline date:").grid(column=1, row=ui_rows,
                                                                            sticky=W)  # rows is last row
new_task_desc_entry = ttk.Entry(mainframe, width=30, textvariable=new_task_desc)
new_task_desc_entry.grid(column=2, row=ui_rows, sticky=(W, E))

new_task_date_entry = ttk.Entry(mainframe, width=16, textvariable=new_task_date)
new_task_date_entry.grid(column=3, row=ui_rows, sticky=(W, E))

ttk.Button(mainframe, text="Add Task", command=add_task).grid(column=4, row=ui_rows, sticky=E)


for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

# task_entry.focus()
#root.bind('<Return>', display_tasks())

root.mainloop()
