from tkinter import *
from tkinter import ttk

import TaskUtil
from Task import Task

UI_COLUMNS = 4
UI_ROWS = 10
START_ROW_INDEX = 2
NUM_OF_TASK_ROWS = 8


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
        # tracks which row task info is started to be populated in
        self.page = 1  # current page of results that is being displayed

        self.tasks = {}  # dict of Task objects
        self.task_rows_dict = {}  # dict used for ui

        root = Tk()
        root.title('To Do List')

        mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(UI_COLUMNS, UI_ROWS))
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.geometry("575x500+300+300")  # window width x window height + position right + position down

        # displays task menu header elements
        header_label_desc = ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=NW)
        header_label_date = ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=NW)
        header_label_delete = ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=N)

        #  displays page navigation ui elements
        # page_displayed_label = ttk.Label(mainframe, textvariable=page_number_text).grid(column=1, row=7, sticky=NW)
        next_button = ttk.Button(mainframe, text="Next tasks",
                                 command=lambda: self.update_page(next_page=True)).grid(column=1, row=8,
                                                                                        sticky=NW)
        prev_button = ttk.Button(mainframe, text="Prev. tasks",
                                 command=lambda: self.update_page(next_page=False)).grid(column=1, row=9,
                                                                                         sticky=NW)

        # generates all task row ui objects and label StringVar values (assigned to ui objects)
        ui_task_rows = {}  # {row int : task object}
        for current_row in range(START_ROW_INDEX, UI_ROWS):
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

        # creates 'add new task' elements
        new_task = Task(StringVar(), StringVar())
        add_task_label = ttk.Label(mainframe, text="Add task description\nand deadline date:").grid(column=1,
                                                                                                    row=UI_ROWS,
                                                                                                    sticky=W)
        new_task_desc_entry = ttk.Entry(mainframe, width=30, textvariable=new_task.desc)
        new_task_desc_entry.grid(column=2, row=UI_ROWS, sticky=(W, E))
        new_task_date_entry = ttk.Entry(mainframe, width=16, textvariable=new_task.date)
        new_task_date_entry.grid(column=3, row=UI_ROWS, sticky=(W, E))
        add_task_button = ttk.Button(mainframe, text="Add Task", command=lambda: add_task(session, new_task)).grid(
            column=4, row=UI_ROWS, sticky=E)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        new_task_desc_entry.focus()
        # root.bind('<Return>', add_task(session, new_task))

        root.mainloop()

    def update_ui_task(self):
        # iterates through each task UI row and updates the UI label string
        for current_row in range(START_ROW_INDEX, UI_ROWS):
            try:
                # checks if tasks[current_row_local] is empty
                # if so set all following task row labels to '', else populate with task info
                # TODO: Add comments to explain the scaled values;
                scaled_task_index = ((self.page - 1) * NUM_OF_TASK_ROWS + current_row) - START_ROW_INDEX
                scaled_ui_row = ((self.page - 1) * UI_ROWS) + current_row
                if scaled_ui_row >= len(self.tasks) + self.page * 2:
                    self.task_rows_dict[current_row].desc.set("")
                    self.task_rows_dict[current_row].date.set("")
                else:
                    self.task_rows_dict[current_row].desc.set(self.tasks[scaled_task_index].task)
                    self.task_rows_dict[current_row].date.set(
                        self.tasks[
                            scaled_task_index].deadline.isoformat())  # converts datetime.date to str MMMM-MM-DD
            except IndexError:  # in case empty query is returned
                pass

    def display_tasks(self, opt, session):
        self.tasks = TaskUtil.get_tasks(session, option=opt)
        self.page = 1  # reset page for new request
        self.update_ui_task()

    def delete_task(self, session, button_index):
        TaskUtil.delete_task(session, self.tasks, button_index)

        # TODO: add popup for invalid task as well as when task is properly deleted

    def update_page(self, next_page=True):
        mod = len(self.tasks) % NUM_OF_TASK_ROWS
        div = len(self.tasks) // 8

        if next_page:  # logic for incrementing current page of info displayed
            if mod == 0:  # no remainder so the last page is fully populated
                if self.page < div:
                    self.page += 1
            else:  # remainder thus last page will be partially filled thus max page > div
                if self.page < div + 1:
                    self.page += 1
        else:  # logic for decrementing current page of info displayed
            if self.page > 1:
                self.page -= 1

        self.update_ui_task()
        '''
        print(len(self.tasks))
        print("mod = {}".format(mod))
        print("div = {}".format(div))
        print(self.page)
        '''
