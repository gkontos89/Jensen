import os
import platform
from tkinter import Tk, Frame

from gui.BrowserSelectionFrame import BrowserSelectionFrame
from gui.LoginFrame import LoginFrame
from gui.ProcessingFrame import ProcessingFrame
from gui.WaitingForQrFrame import WaitingForQrFrame
from web.Driver import Driver


class Jensen(Tk):
    def __init__(self):
        super().__init__()
        self.main_container = Frame(self)
        self.main_container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        self.driver = Driver()

        # Add web driver executable to path
        driver_path = os.path.join(os.getcwd(), 'tools', 'win' if platform.system() == 'Windows' else 'mac')
        current_path = os.environ['Path']
        if driver_path not in current_path:
            os.environ['Path'] += os.pathsep + driver_path

        for frame in (BrowserSelectionFrame, LoginFrame, ProcessingFrame, WaitingForQrFrame):
            frame_name = frame.__name__
            f = frame(parent=self.main_container, controller=self, width=50, driver=self.driver)
            self.frames[frame_name] = f
            f.grid(row=0, column=0, sticky='nsew')

        self.show_frame('BrowserSelectionFrame')

    def show_frame(self, frame_name, **kwargs):
        frame = self.frames[frame_name]
        frame.tkraise()
        if isinstance(frame, ProcessingFrame):
            client_name = kwargs['client_name']
            form = kwargs['form']
            frame.start_processing(client_name, form)
        elif isinstance(frame, WaitingForQrFrame):
            frame.start_waiting_for_qr()


if __name__ == '__main__':
    root = Jensen()
    root.geometry('500x500')
    root.mainloop()
