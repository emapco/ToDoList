from DBTool import create_engine_session
from UI import UI

class App:
    def __init__(self):
        session = create_engine_session()  # create db engine and return session
        ui = UI(session)

app = App()
