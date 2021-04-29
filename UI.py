from tkinter import *
from tkinter import ttk

import TaskUtil
from Task import Task


def add_task(session, task):
    try:
        TaskUtil.add_task(session, task)

        # TODO: add popup confirmation screen and set fields to '' after adding
    except ValueError:
        # TODO: add popup error screen (for date formatting issues)
        pass
    pass


class UI:
    def __init__(self, session):
        self.ui_columns = 4
        self.ui_rows = 10
        self.start_row_index = 2  # tracks which row task info is started to be populated

        self.tasks = {}  # dict of Task objects
        self.task_rows_dict = {}  # dict used for ui

        root = Tk()
        root.title('To Do List')

        mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(self.ui_columns, self.ui_rows))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.geometry("575x500+300+300")  # window width x window height + position right + position down

        # displays task menu header
        header_label_desc = ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=NW)
        header_label_date = ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=NW)
        header_label_delete = ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=N)

        # displays page navigation
        nav_task_label = ttk.Label(mainframe, text="Nav. tasks").grid(column=1, row=7, sticky=NW)
        next_button = ttk.Button(mainframe, text="Next tasks").grid(column=1, row=8, sticky=NW)
        prev_button = ttk.Button(mainframe, text="Prev. tasks").grid(column=1, row=9, sticky=NW)

        # generates all task row ui objects and label StringVar values (assigned to ui objects)
        ui_task_rows = {}  # {row int : task object}
        for current_row in range(self.start_row_index, self.ui_rows):
            self.task_rows_dict[current_row] = Task(StringVar(), StringVar())  # current_row-2 since range starts on 2

            ui_task_rows[current_row] = [
                ttk.Label(mainframe, textvariable=self.task_rows_dict[current_row].desc).grid(column=2,
                                                                                              row=current_row),
                ttk.Label(mainframe, textvariable=self.task_rows_dict[current_row].date).grid(column=3,
                                                                                              row=current_row),
                ttk.Button(mainframe, text="Del. Task",
                           command=lambda button_index=current_row - 2:
                           self.delete_task(session, button_index)).grid(column=4, row=current_row, sticky=E)
            ]  # (current_row - 1) is 1-based index for UI; List is zero-based so (current_row-2)

        # creates request task buttons and label
        display_label = ttk.Label(mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=W)
        today_task_button = ttk.Button(mainframe, text="Today\'s tasks",
                                       command=lambda: self.display_tasks(1, session)).grid(column=1, row=2, sticky=W)
        week_task_button = ttk.Button(mainframe, text="Week\'s tasks",
                                      command=lambda: self.display_tasks(2, session)).grid(column=1, row=3, sticky=W)
        all_task_button = ttk.Button(mainframe, text="All tasks",
                                     command=lambda: self.display_tasks(3, session)).grid(column=1, row=4, sticky=W)
        missed_task_button = ttk.Button(mainframe, text="Missed tasks",
                                        command=lambda: self.display_tasks(4, session)).grid(column=1, row=5, sticky=W)

        # creates add new task elements
        new_task = Task(StringVar(), StringVar())
        add_task_label = ttk.Label(mainframe, text="Add task description\nand deadline date:").grid(column=1,
                                                                                                    row=self.ui_rows,
                                                                                                    sticky=W)
        new_task_desc_entry = ttk.Entry(mainframe, width=30, textvariable=new_task.desc)
        new_task_desc_entry.grid(column=2, row=self.ui_rows, sticky=(W, E))
        new_task_date_entry = ttk.Entry(mainframe, width=16, textvariable=new_task.date)
        new_task_date_entry.grid(column=3, row=self.ui_rows, sticky=(W, E))
        add_task_button = ttk.Button(mainframe, text="Add Task", command=lambda: add_task(session, new_task)).grid(
            column=4,
            row=self.ui_rows,
            sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        new_task_desc_entry.focus()
        root.bind('<Return>', add_task(session, new_task))

        root.mainloop()

    def update_ui_task(self):
        for current_row in range(self.start_row_index, self.ui_rows):
            try:  # catch IndexError in case empty query is returned
                # checks if tasks[current_row_local] is empty (by checking if all tasks elements have already be added)
                # if so set all following task row labels to '', else populate with task info
                if current_row >= self.start_row_index + len(self.tasks):
                    self.task_rows_dict[current_row].desc.set("")
                    self.task_rows_dict[current_row].date.set("")
                else:
                    self.task_rows_dict[current_row].desc.set(self.tasks[current_row - 2].task)
                    self.task_rows_dict[current_row].date.set(
                        self.tasks[
                            current_row - 2].deadline.isoformat())  # converts datetime.date to str MMMM-MM-DD
            except IndexError:
                pass

    def display_tasks(self, opt, session):
        self.tasks = TaskUtil.get_tasks(session, option=opt)  # [[index, task desc str, task date str],[]]
        self.update_ui_task()

    def delete_task(self, session, button_index):
        TaskUtil.delete_task(session, self.tasks, button_index)

        # TODO: add popup for invalid task as well as when task is properly deleted
