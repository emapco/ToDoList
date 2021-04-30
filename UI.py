import tkinter as ttkk
from tkinter import ttk
from tkinter import messagebox as mb

import TaskUtil
from Task import Task

UI_COLUMNS = 4
UI_ROWS = 10
START_ROW_INDEX = 2
NUM_OF_TASK_ROWS = 8


def display_error_message(message):
    mb.showerror("Error", message)


def display_confirm_message(message):
    mb.showinfo("", message)


def get_scaled_task_index(task_page, row_index):
    return (task_page - 1) * NUM_OF_TASK_ROWS + row_index


class UI:
    def __init__(self, session):
        self.task_page = 1
        self.tasks = {}
        self.task_ui_stringvar_dict = {}

        root = ttkk.Tk()
        root.title('To Do List')

        mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(UI_COLUMNS, UI_ROWS))
        mainframe.grid(column=0, row=0, sticky=(ttkk.N, ttkk.W, ttkk.E, ttkk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.geometry("575x500+300+300")  # window width x window height + position right + position down

        self.display_menu_header_elements(mainframe)
        self.display_navigation_UI_elements(mainframe)
        self.display_task_query_elements(mainframe, session)
        self.display_task_info_elements(mainframe, session)
        self.display_add_new_task_elements(mainframe, session)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # root.bind('<Return>', add_task(session, new_task))
        root.mainloop()

    def display_navigation_UI_elements(self, mainframe):
        # page_displayed_label = ttk.Label(mainframe, textvariable=page_number_text).grid(column=1, row=7, sticky=NW)
        next_button = ttk.Button(mainframe, text="Next tasks",
                                 command=lambda: self.update_page(next_page=True)).grid(column=1, row=8, sticky=ttkk.NW)
        prev_button = ttk.Button(mainframe, text="Prev. tasks",
                                 command=lambda: self.update_page(next_page=False)).grid(column=1, row=9,
                                                                                         sticky=ttkk.NW)

    def display_menu_header_elements(self, mainframe):
        header_label_desc = ttk.Label(mainframe, text="Task Description").grid(column=2, row=1, sticky=ttkk.NW)
        header_label_date = ttk.Label(mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1, sticky=ttkk.NW)
        header_label_delete = ttk.Label(mainframe, text="Delete").grid(column=4, row=1, sticky=ttkk.N)

    def display_task_query_elements(self, mainframe, session):
        display_label = ttk.Label(mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=ttkk.W)
        today_task_button = ttk.Button(mainframe, text="Today\'s tasks",
                                       command=lambda: self.display_tasks(1, session)).grid(column=1, row=2,
                                                                                            sticky=ttkk.W)
        week_task_button = ttk.Button(mainframe, text="Week\'s tasks",
                                      command=lambda: self.display_tasks(2, session)).grid(column=1, row=3,
                                                                                           sticky=ttkk.W)
        all_task_button = ttk.Button(mainframe, text="All tasks",
                                     command=lambda: self.display_tasks(3, session)).grid(column=1, row=4,
                                                                                          sticky=ttkk.W)
        missed_task_button = ttk.Button(mainframe, text="Missed tasks",
                                        command=lambda: self.display_tasks(4, session)).grid(column=1, row=5,
                                                                                             sticky=ttkk.W)

    def display_task_info_elements(self, mainframe, session):
        ui_task_rows = {}  # {row int : task object}
        for current_row in range(START_ROW_INDEX, UI_ROWS):
            self.task_ui_stringvar_dict[current_row] = Task(ttkk.StringVar(), ttkk.StringVar())

            ui_task_rows[current_row] = [
                ttk.Label(mainframe, textvariable=self.task_ui_stringvar_dict[current_row].desc).grid(column=2,
                                                                                                      row=current_row),
                ttk.Label(mainframe, textvariable=self.task_ui_stringvar_dict[current_row].date).grid(column=3,
                                                                                                      row=current_row),
                ttk.Button(mainframe, text="Del. Task",
                           command=lambda button_index=current_row - 2:
                           self.delete_task(session, button_index)).grid(column=4, row=current_row, sticky=ttkk.E)
            ]  # (current_row - 1) is 1-based index for UI; List is zero-based so (current_row-2)

    def display_add_new_task_elements(self, mainframe, session):
        new_task = Task(ttkk.StringVar(), ttkk.StringVar())
        add_task_label = ttk.Label(mainframe, text="Add task description\nand deadline date:").grid(column=1,
                                                                                                    row=UI_ROWS,
                                                                                                    sticky=ttkk.W)
        new_task_desc_entry = ttk.Entry(mainframe, width=30, textvariable=new_task.desc)
        new_task_desc_entry.grid(column=2, row=UI_ROWS, sticky=(ttkk.W, ttkk.E))
        new_task_date_entry = ttk.Entry(mainframe, width=16, textvariable=new_task.date)
        new_task_date_entry.grid(column=3, row=UI_ROWS, sticky=(ttkk.W, ttkk.E))
        add_task_button = ttk.Button(mainframe, text="Add Task", command=lambda: self.add_task(session, new_task)).grid(
            column=4, row=UI_ROWS, sticky=ttkk.E)
        new_task_desc_entry.focus()

    def update_ui_task(self):
        # iterates through each task UI row and updates the UI label string
        for current_row in range(START_ROW_INDEX, UI_ROWS):
            try:
                # checks if tasks[current_row_local] is empty
                # if so set all following task row labels to '', else populate with task info
                # TODO: Add comments to explain the scaled values;
                # get_scaled_task_index subtracted by START_ROW_INDEX since range starts on START_ROW_INDEX
                scaled_task_index = get_scaled_task_index(self.task_page, current_row) - START_ROW_INDEX
                scaled_ui_row = (self.task_page - 1) * UI_ROWS + current_row
                if scaled_ui_row >= len(self.tasks) + self.task_page * 2:
                    self.task_ui_stringvar_dict[current_row].desc.set("")
                    self.task_ui_stringvar_dict[current_row].date.set("")
                else:
                    self.task_ui_stringvar_dict[current_row].desc.set(self.tasks[scaled_task_index].task)
                    self.task_ui_stringvar_dict[current_row].date.set(
                        self.tasks[
                            scaled_task_index].deadline.isoformat())  # converts datetime.date to str MMMM-MM-DD
            except IndexError:  # in case empty query is returned
                pass

    def display_tasks(self, opt, session):
        self.tasks = TaskUtil.get_tasks(session, option=opt)
        self.task_page = 1  # reset page for new request
        self.update_ui_task()

    def add_task(self, session, task):
        result = TaskUtil.add_task(session, task)
        if result == 1:
            display_confirm_message("Task has been added")
        else:
            display_error_message("Invalid date")

    def delete_task(self, session, button_index):
        result = TaskUtil.delete_task(session, self.tasks, get_scaled_task_index(self.task_page, button_index))
        if result == 1:
            display_confirm_message("Task has been deleted")
        else:
            display_error_message("Task has already been deleted")

    def update_page(self, next_page=True):
        mod = len(self.tasks) % NUM_OF_TASK_ROWS
        div = len(self.tasks) // NUM_OF_TASK_ROWS

        if next_page:  # logic for incrementing current page of info displayed
            if mod == 0:  # no remainder so the last page is fully populated thus last page = div
                if self.task_page < div:
                    self.task_page += 1
            else:  # remainder thus last page will be partially filled thus last page = div + 1
                if self.task_page < div + 1:
                    self.task_page += 1
        else:
            if self.task_page > 1:
                self.task_page -= 1

        self.update_ui_task()
