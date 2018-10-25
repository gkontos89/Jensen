from tkinter import Tk

from gui.BrowserSelectionFrame import BrowserSelectionFrame
from web.Driver import Driver

if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    driver = Driver()
    browser_selection_frame = BrowserSelectionFrame(root, 75, driver)
    browser_selection_frame.pack()
    root.mainloop()
