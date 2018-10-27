from tkinter import Label, Entry, Button, Tk

from selenium.common.exceptions import NoSuchElementException

from gui.BaseFrame import BaseFrame


class LoginFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.username_label = Label(self, text='Username')
        self.username_text_entry = Entry(self, width='50')
        self.username_text_entry.insert(0, 'sam.jensen@bairdwarner.com')  # TODO get default from file or pickle
        self.password_label = Label(self, text='Password')
        self.password_text_entry = Entry(self, width='50', show='*')
        self.password_text_entry.insert(0, 'develop23')  # TODO get default from file or pickle
        self.invalid_login_notification_text = Label(self, text='Invalid Login')
        self.login_button = Button(self, text='Login', command=self.login_button_command)
        self.back_button = Button(self, text='Back', command=self.back_button_command)
        self.username_label.pack()
        self.username_text_entry.pack()
        self.password_label.pack()
        self.password_text_entry.pack()
        self.invalid_login_notification_text.pack()
        self.invalid_login_notification_text.pack_forget()
        self.login_button.pack()
        self.back_button.pack()

    def login_button_command(self):
        # Handle if we are recovering from an invalid login and are already at the login screen
        try:
            self.driver.go_to_login_screen()
        except NoSuchElementException:
            pass

        self.driver.enter_username(self.username_text_entry.get())
        self.driver.enter_password(self.password_text_entry.get())
        self.driver.press_login_button()
        try:
            self.driver.check_for_valid_credentials()
            self.invalid_login_notification_text.pack_forget()
            self.controller.show_frame('WaitingForQrFrame')
        except NoSuchElementException:
            self.invalid_login_notification_text.pack()

    def back_button_command(self):
        self.driver.close_web_driver()
        self.controller.show_frame('BrowserSelectionFrame')


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = LoginFrame(root, root, 50)
    base_frame.pack()
    root.mainloop()

