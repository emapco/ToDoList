from datetime import datetime

from tkinter import *
from tkinter import ttk

from DBTool import create_engine_session
import TaskUtil


# menu buttons functions
def display_today_tasks():
    tasks = TaskUtil.get_tasks(session, option=1)  # list [[index, task desc str, task date str],[]]
    update_ui_task(tasks)
    pass


def display__week_tasks():
    tasks = TaskUtil.get_tasks(session, option=2)
    update_ui_task(tasks)
    pass


def display_all_tasks():
    tasks = TaskUtil.get_tasks(session, option=3)
    update_ui_task(tasks)
    pass


def display_missed_tasks():
    tasks = TaskUtil.get_tasks(session, option=4)
    update_ui_task(tasks)
    pass


# displaying tasks in ui rows [2,9] nad columns [2:3]
def update_ui_task(tasks):
    for current_row_local in range(start_row_index, ui_rows):
        try:  # catch IndexError in case empty query is returned
            global task_string_rows

            # checks if tasks[current_row_local] is empty (by checking if all tasks elements have already be added)
            # if so set all following task row labels to '', else populate with task info
            if current_row_local >= start_row_index + len(tasks):
                task_string_rows[current_row_local][0].set("")
                task_string_rows[current_row_local][1].set("")
            else:
                task_string_rows[current_row_local][0].set(tasks[current_row_local - 2][1])
                task_string_rows[current_row_local][1].set(
                    tasks[current_row_local - 2][2].isoformat())  # converts datetime.date to str MMMM-MM-DD
        except IndexError:
            pass
    pass


# add new task button functionality
def add_task():
    try:
        task_desc = new_task_desc.get()
        task_date = datetime.strptime(new_task_date.get(), '%Y-%m-%d')

        TaskUtil.add_task(session, task_desc, task_date)

        # add popup confirmation screen and set fields to '' after adding
    except ValueError:
        # add popup error screen (for date formatting issues)
        pass
    pass


# del task button functionality
def delete_task():
    pass


session = create_engine_session()  # create db engine and return session
ui_columns = 4
ui_rows = 10
start_row_index = 2

root = Tk()
root.title('To Do List')

mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(ui_columns, ui_rows))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

root.geometry("575x500+300+300")  # window width x window height + position right + position down

new_task_desc = StringVar()
new_task_date = StringVar()

# displays task menu header
header_label_desc = ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=NW)
header_label_date = ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=NW)
header_label_delete = ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=N)

# generates all task row ui objects and label StringVar values (assigned to ui objects)
task_ui_rows = {}  # {current_row : [task desc , task date] }
task_string_rows = {}  # {current_row : [task desc , task date] }
for current_row in range(start_row_index, ui_rows):
    task_string_rows[current_row] = [StringVar(), StringVar()]  # current_row-2 since range starts on 2

    task_ui_rows[current_row] = [
        ttk.Label(mainframe, textvariable=task_string_rows[current_row][0]).grid(column=2, row=current_row),
        ttk.Label(mainframe, textvariable=task_string_rows[current_row][1]).grid(column=3, row=current_row),
        ttk.Button(mainframe, text="Del", command=delete_task).grid(column=4, row=current_row, sticky=E)
    ]

# creates request task buttons and label
display_label = ttk.Label(mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=W)
today_task_button = ttk.Button(mainframe, text="Today\'s tasks", command=display_today_tasks).grid(column=1, row=2,
                                                                                                   sticky=W)
week_task_button = ttk.Button(mainframe, text="Week\'s tasks", command=display__week_tasks).grid(column=1, row=3,
                                                                                                 sticky=W)
all_task_button = ttk.Button(mainframe, text="All tasks", command=display_all_tasks).grid(column=1, row=4, sticky=W)
missed_task_button = ttk.Button(mainframe, text="Missed tasks", command=display_missed_tasks).grid(column=1, row=5,
                                                                                                   sticky=W)

# creates add new task elements
add_task_label = ttk.Label(mainframe, text="Add task description \nand deadline date:").grid(column=1, row=ui_rows,
                                                                                         sticky=W)
new_task_desc_entry = ttk.Entry(mainframe, width=30, textvariable=new_task_desc)
new_task_desc_entry.grid(column=2, row=ui_rows, sticky=(W, E))
new_task_date_entry = ttk.Entry(mainframe, width=16, textvariable=new_task_date)
new_task_date_entry.grid(column=3, row=ui_rows, sticky=(W, E))
add_task_button = ttk.Button(mainframe, text="Add Task", command=add_task).grid(column=4, row=ui_rows, sticky=E)

for child in mainframe.winfo_children(): child.grid_configure(padx=10, pady=10)

new_task_desc_entry.focus()
root.bind('<Return>', add_task())

root.mainloop()
