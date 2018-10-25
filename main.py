from tkinter import Tk, Frame

from gui.BrowserSelectionFrame import BrowserSelectionFrame
from gui.LoginFrame import LoginFrame
from web.Driver import Driver


class Jensen(Tk):
    def __init__(self):
        super().__init__()
        self.main_container = Frame(self)
        self.main_container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        self.driver = Driver()
        for frame in (BrowserSelectionFrame, LoginFrame):
            frame_name = frame.__name__
            f = frame(parent=self.main_container, controller=self, width=50, driver=self.driver)
            self.frames[frame_name] = f
            f.grid(row=0, column=0, sticky='nsew')

        self.show_frame('BrowserSelectionFrame')

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

if __name__ == '__main__':
    root = Jensen()
    root.geometry('500x500')

    # driver = Driver()
    # browser_selection_frame = BrowserSelectionFrame(root, 75, driver)
    # browser_selection_frame.pack()
    root.mainloop()
