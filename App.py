from datetime import datetime

from tkinter import *
from tkinter import ttk

from DBTool import create_engine_session
import TaskUtil


# task menu button function
def display_tasks(opt):
    global tasks
    global rows
    tasks, rows = TaskUtil.get_tasks(session, option=opt)  # [[index, task desc str, task date str],[]]
    update_ui_task()
    pass


# displaying tasks in ui rows [2,9] nad columns [2:3]
def update_ui_task():
    global tasks
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
def delete_task(index):
    global rows
    TaskUtil.delete_task(session, rows, index)
    pass


session = create_engine_session()  # create db engine and return session
tasks = []  # [[index, task desc str, task date str],[]]
rows = ()
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


# displays task menu header
header_label_desc = ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=NW)
header_label_date = ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=NW)
header_label_delete = ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=N)

# generates all task row ui objects and label StringVar values (assigned to ui objects)
task_ui_rows = {}  # {row : [task desc , task date] }
task_string_rows = {}  # {row : [task desc , task date] }
for current_row in range(start_row_index, ui_rows):
    task_string_rows[current_row] = [StringVar(), StringVar()]  # current_row-2 since range starts on 2

    task_ui_rows[current_row] = [
        ttk.Label(mainframe, textvariable=task_string_rows[current_row][0]).grid(column=2, row=current_row),
        ttk.Label(mainframe, textvariable=task_string_rows[current_row][1]).grid(column=3, row=current_row),
        ttk.Button(mainframe, text="Del {}" .format(current_row-1),
                   command=lambda button_index=current_row-2: delete_task(button_index)).grid(column=4, row=current_row, sticky=E)
    ]  # (current_row - 1) is 1-based index for UI; List is zero-based so (current_row-2)

# creates request task buttons and label
display_label = ttk.Label(mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=W)
today_task_button = ttk.Button(mainframe, text="Today\'s tasks", command=lambda: display_tasks(1)).grid(column=1, row=2,
                                                                                                   sticky=W)
week_task_button = ttk.Button(mainframe, text="Week\'s tasks", command=lambda: display_tasks(2)).grid(column=1, row=3,
                                                                                                 sticky=W)
all_task_button = ttk.Button(mainframe, text="All tasks", command=lambda: display_tasks(3)).grid(column=1, row=4, sticky=W)
missed_task_button = ttk.Button(mainframe, text="Missed tasks", command=lambda: display_tasks(4)).grid(column=1, row=5,
                                                                                                   sticky=W)

# creates add new task elements
new_task_desc = StringVar()
new_task_date = StringVar()

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
