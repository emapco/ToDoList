from DBTool import TaskDatabase
from UI import UI


class App:
    def __init__(self):
        db = TaskDatabase()
        ui = UI(db)


if __name__ == "__main__":
    app = App()
