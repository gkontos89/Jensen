from tkinter import Label, Button

from gui.BaseFrame import BaseFrame


class WaitingForQrFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.waiting_for_login_text = Label(self, text='Waiting for QR Login...')
        self.go_to_surveys_button = Button(self, text='Go to Surveys', command=self.go_to_surveys_button_command)
        self.waiting_for_login_text.pack()
        self.waiting_for_login_text.pack_forget()
        self.go_to_surveys_button.pack()

    def start_waiting_for_qr(self):
        self.waiting_for_login_text.pack()
        self.go_to_surveys_button.pack_forget()
        while not self.driver.home_page_has_loaded():
            # Sit and wait for the home page to load
            pass

    def go_to_surveys_button_command(self):
        self.waiting_for_login_text.pack()
        while not self.driver.home_page_has_loaded():
            # Sit and wait for the home page to load
            pass
        self.driver.open_menu()
        self.driver.go_to_surveys()
        self.controller.show_frame('SurveyFrame')




