import os
import platform
from tkinter import Button, Tk, PhotoImage, Label, LEFT

from gui.BaseFrame import BaseFrame
from utilities.JensenLogger import JensenLogger
from web.CoreDriver import WebBrowser

WEB_BUTTON_WIDTH = '80'
WEB_BUTTON_HEIGHT = '80'


class BrowserSelectionFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.instructions = Label(self, text='Welcome to Jensen!  Please select your preferred web browser below')
        self.instructions.config(pady=20)
        this_directory = os.path.dirname(__file__)
        firefox_logo_path = os.path.join(this_directory, '../img/firefox.png')
        self.firefox_logo = PhotoImage(file=firefox_logo_path)
        self.firefox_button = Button(self, image=self.firefox_logo,
                                     command=self.firefox_button_command,
                                     width=WEB_BUTTON_WIDTH,
                                     height=WEB_BUTTON_HEIGHT)
        chrome_logo_path = os.path.join(this_directory, '../img/chrome.png')
        self.chrome_logo = PhotoImage(file=chrome_logo_path)
        self.chrome_button = Button(self, image=self.chrome_logo,
                                    command=self.chrome_button_command,
                                    width=WEB_BUTTON_WIDTH,
                                    height=WEB_BUTTON_HEIGHT)
        edge_logo_path = os.path.join(this_directory, '../img/edge.png')
        self.edge_logo = PhotoImage(file=edge_logo_path)
        self.edge_button = Button(self, image=self.edge_logo,
                                  command=self.edge_button_command,
                                  width=WEB_BUTTON_WIDTH,
                                  height=WEB_BUTTON_HEIGHT)
        safari_logo_path = os.path.join(this_directory, '../img/safari.png')
        self.safari_logo = PhotoImage(file=safari_logo_path)
        self.safari_button = Button(self, image=self.safari_logo,
                                    command=self.safari_button_command,
                                    width=WEB_BUTTON_WIDTH,
                                    height=WEB_BUTTON_HEIGHT)
        self.instructions.pack()
        self.firefox_button.pack(side=LEFT)
        self.chrome_button.pack(side=LEFT)
        self.edge_button.pack(side=LEFT)
        self.safari_button.pack(side=LEFT)

    def firefox_button_command(self):
        try:
            self.driver.configure_web_driver(WebBrowser.FIREFOX)
            self.driver.go_to_costar()
            self.controller.show_frame('LoginFrame')
        except:
            JensenLogger.get_instance().log_exception('Error trying to launch Firefox browser')
            JensenLogger.get_instance().log_warning('Ensure Firefox Version 63.0.0+ is installed')

    def chrome_button_command(self):
        try:
            self.driver.configure_web_driver(WebBrowser.CHROME)
            self.driver.go_to_costar()
            self.controller.show_frame('LoginFrame')
        except:
            JensenLogger.get_instance().log_exception('Error trying to launch Chrome browser')

    def edge_button_command(self):
        pass
        # self.driver.configure_web_driver(WebBrowser.EDGE)
        # self.driver.go_to_costar()

    def safari_button_command(self):
        try:
            self.driver.configure_web_driver(WebBrowser.SAFARI)
            self.driver.go_to_costar()
            self.controller.show_frame('LoginFrame')
        except:
            JensenLogger.get_instance().log_exception('Error trying to launch Safari browser')

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = BrowserSelectionFrame(root, root, 50)
    base_frame.pack()
    root.mainloop()
