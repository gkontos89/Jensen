from gui.BaseFrame import BaseFrame


class SurveyFrame(BaseFrame):
    def __init__(self, parent, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.driver = driver


