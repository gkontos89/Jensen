import os
from tkinter import Button, Tk, PhotoImage, Label, LEFT

from gui.BaseFrame import BaseFrame
from web.Driver import WebBrowser


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
                                     width='120',
                                     height='120')
        chrome_logo_path = os.path.join(this_directory, '../img/chrome.png')
        self.chrome_logo = PhotoImage(file=chrome_logo_path)
        self.chrome_button = Button(self, image=self.chrome_logo,
                                    command=self.chrome_button_command,
                                    width='120',
                                    height='120')
        edge_logo_path = os.path.join(this_directory, '../img/edge.png')
        self.edge_logo = PhotoImage(file=edge_logo_path)
        self.edge_button = Button(self, image=self.edge_logo,
                                  command=self.edge_button_command,
                                  width='120',
                                  height='120')
        self.instructions.pack()
        self.firefox_button.pack(side=LEFT)
        self.chrome_button.pack(side=LEFT)
        self.edge_button.pack(side=LEFT)

    def firefox_button_command(self):
        self.driver.configure_web_driver(WebBrowser.FIREFOX)
        self.driver.go_to_costar()
        self.controller.show_frame('LoginFrame')

    def chrome_button_command(self):
        pass
        # self.driver.configure_web_driver(WebBrowser.CHROME)
        # self.driver.go_to_costar()

    def edge_button_command(self):
        pass
        # self.driver.configure_web_driver(WebBrowser.EDGE)
        # self.driver.go_to_costar()


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = BrowserSelectionFrame(root, 50)
    base_frame.pack()
    root.mainloop()
