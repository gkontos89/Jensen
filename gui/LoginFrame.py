from tkinter import Label, Entry, Button, Tk

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
        self.login_button = Button(self, text='Login', command=self.login_button_command)
        self.back_button = Button(self, text='Back') # TODO set to controller.show_frame browswerslection
        self.username_label.pack()
        self.username_text_entry.pack()
        self.password_label.pack()
        self.password_text_entry.pack()
        self.login_button.pack()

    def login_button_command(self):
        # TODO add try catch for failed login
        self.driver.go_to_login_screen()
        self.driver.enter_username(self.username_text_entry.get())
        self.driver.enter_password(self.password_text_entry.get())
        self.driver.press_login_button()


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = LoginFrame(root, 50)
    base_frame.pack()
    root.mainloop()

