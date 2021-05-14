import tkinter as ttkk
from tkinter import ttk
from tkinter import messagebox as mb

from DBTool import TODAY_TASK_OPTION, WEEK_TASK_OPTION, ALL_TASK_OPTION, MISSED_TASK_OPTION, TaskDatabase
from Task import Task

UI_COLUMNS = 4
UI_ROWS = 10
START_ROW_INDEX = 2
NUM_OF_TASK_ROWS = 8


class UI:
    def __init__(self, db):
        """
        Initiator

        Parameters:
        -----------
        db: TaskDatabase
            The database session object the UI stores and retrieves data from
        """
        self.task_page = 1
        self.tasks = {}
        self.task_ui_stringvar_dict = {}

        root = ttkk.Tk()
        root.title('To Do List')

        self.mainframe = ttk.Frame(root, padding='{0} {1} 12 12'.format(UI_COLUMNS, UI_ROWS))
        self.mainframe.grid(column=0, row=0, sticky=(ttkk.N, ttkk.W, ttkk.E, ttkk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        root.geometry("575x500+300+300")  # window width x window height + position right + position down

        self._display_menu_header_elements()
        self._display_navigation_UI_elements()
        self._display_task_query_elements(db)
        self._display_task_info_elements(db)
        self._display_add_new_task_elements(db)

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=10, pady=10)

        # root.bind('<Return>', add_task(session, new_task))
        root.mainloop()

    """
    ##########################################################################
                                Private Functions
    ##########################################################################
    """
    def _display_navigation_UI_elements(self) -> None:
        # page_displayed_label = ttk.Label(mainframe, textvariable=page_number_text).grid(column=1, row=7, sticky=NW)
        next_button = ttk.Button(self.mainframe, text="Next tasks",
                                 command=lambda: self._update_page(next_page=True)).grid(column=1, row=8, sticky=ttkk.NW)
        prev_button = ttk.Button(self.mainframe, text="Prev. tasks",
                                 command=lambda: self._update_page(next_page=False)).grid(column=1, row=9,
                                                                                          sticky=ttkk.NW)

    def _display_menu_header_elements(self) -> None:
        header_label_desc = ttk.Label(self.mainframe, text="Task Description").grid(column=2, row=1, sticky=ttkk.NW)
        header_label_date = ttk.Label(self.mainframe, text="Deadline\n(YYYY-MM-DD)").grid(column=3, row=1,
                                                                                          sticky=ttkk.NW)
        header_label_delete = ttk.Label(self.mainframe, text="Delete").grid(column=4, row=1, sticky=ttkk.N)

    def _display_task_query_elements(self, db: TaskDatabase) -> None:
        display_label = ttk.Label(self.mainframe, text="Display\n(click one):").grid(column=1, row=1, sticky=ttkk.W)
        today_task_button = ttk.Button(self.mainframe, text="Today\'s tasks",
                                       command=lambda: self._display_tasks(TODAY_TASK_OPTION, db)).grid(column=1, row=2,
                                                                                                        sticky=ttkk.W)
        week_task_button = ttk.Button(self.mainframe, text="Week\'s tasks",
                                      command=lambda: self._display_tasks(WEEK_TASK_OPTION, db)).grid(column=1, row=3,
                                                                                                      sticky=ttkk.W)
        all_task_button = ttk.Button(self.mainframe, text="All tasks",
                                     command=lambda: self._display_tasks(ALL_TASK_OPTION, db)).grid(column=1, row=4,
                                                                                                    sticky=ttkk.W)
        missed_task_button = ttk.Button(self.mainframe, text="Missed tasks",
                                        command=lambda: self._display_tasks(MISSED_TASK_OPTION, db)).grid(column=1,
                                                                                                          row=5,
                                                                                                          sticky=ttkk.W)

    def _display_task_info_elements(self, db: TaskDatabase) -> None:
        ui_task_rows = {}  # {row int : task object}
        for current_row in range(START_ROW_INDEX, UI_ROWS):
            self.task_ui_stringvar_dict[current_row] = Task(ttkk.StringVar(), ttkk.StringVar())

            ui_task_rows[current_row] = [
                ttk.Label(self.mainframe, textvariable=self.task_ui_stringvar_dict[current_row].desc).grid(column=2,
                                                                                                           row=current_row),
                ttk.Label(self.mainframe, textvariable=self.task_ui_stringvar_dict[current_row].date).grid(column=3,
                                                                                                           row=current_row),
                ttk.Button(self.mainframe, text="Del. Task",
                           command=lambda button_index=current_row - 2:
                           self._delete_task(db, button_index)).grid(column=4, row=current_row, sticky=ttkk.E)
            ]  # (current_row - 1) is 1-based index for UI; List is zero-based so (current_row-2)

    def _display_add_new_task_elements(self, db: TaskDatabase) -> None:
        new_task = Task(ttkk.StringVar(), ttkk.StringVar())
        add_task_label = ttk.Label(self.mainframe, text="Add task description\nand deadline date:").grid(column=1,
                                                                                                         row=UI_ROWS,
                                                                                                         sticky=ttkk.W)
        new_task_desc_entry = ttk.Entry(self.mainframe, width=30, textvariable=new_task.desc)
        new_task_desc_entry.grid(column=2, row=UI_ROWS, sticky=(ttkk.W, ttkk.E))
        new_task_date_entry = ttk.Entry(self.mainframe, width=16, textvariable=new_task.date)
        new_task_date_entry.grid(column=3, row=UI_ROWS, sticky=(ttkk.W, ttkk.E))
        add_task_button = ttk.Button(self.mainframe, text="Add Task", command=lambda: self._add_task(db, new_task)).grid(
            column=4, row=UI_ROWS, sticky=ttkk.E)
        new_task_desc_entry.focus()

    def _display_tasks(self, option: int, db: TaskDatabase) -> None:
        """Returns tasks based on button pressed (option selected)
        and assigns the tasks to self.tasks

        Arguments:
        option -- type of request
        db -- database where tasks are stored
        """
        self.tasks = db.get_tasks(option)
        self.task_page = 1  # reset page for new request
        self._update_ui_task()

    def _add_task(self, db: TaskDatabase, task: Task) -> None:
        """Attempts to add task to database. If successful then
        display confirmation message otherwise display error message

        Arguments:
        db -- database where tasks are stored
        task -- task object to be added to database
        """
        result = db.add_task(task)
        if result:
            self._display_confirm_message("Task has been added")
        else:
            self._display_error_message("Invalid date")

    def _delete_task(self, db: TaskDatabase, button_index: int) -> None:
        """Attempts to remove task from database. If successful then
        display confirmation message otherwise display error message

        Arguments:
        db -- database where tasks are stored
        button_index -- index of button pressed and index of the task to be deleted
        """
        result = db.delete_task(self.tasks, self._get_scaled_task_index(self.task_page, button_index))
        if result:
            self._display_confirm_message("Task has been deleted")
        else:
            self._display_error_message("Task has already been deleted")

    def _update_ui_task(self) -> None:
        """Updates the UI's stringvar variables used to display task information
        with the tasks retrieved from the database.
        """
        # iterates through each task UI row and updates the UI label string
        for current_row in range(START_ROW_INDEX, UI_ROWS):
            try:
                # checks if tasks[current_row_local] is empty
                # if so set all following task row labels to '', else populate with task info
                # TODO: Add comments to explain the scaled values;
                # get_scaled_task_index subtracted by START_ROW_INDEX since range starts on START_ROW_INDEX
                scaled_task_index = self._get_scaled_task_index(self.task_page, current_row) - START_ROW_INDEX
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

    def _update_page(self, next_page: bool) -> None:
        """Attempts to update the current page of task displayed and then
        updates the UI with the new tasks

        Arguments:
        next_page -- boolean if user tried to load the next page of tasks
        """
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

        self._update_ui_task()

    """
    ##########################################################################
                                Static Functions
    ##########################################################################
    """

    @staticmethod
    def _display_error_message(message):
        mb.showerror("Error", message)

    @staticmethod
    def _display_confirm_message(message):
        mb.showinfo("", message)

    @staticmethod
    def _get_scaled_task_index(task_page, row_index):
        return (task_page - 1) * NUM_OF_TASK_ROWS + row_index
