import os
import platform
import sys
import threading
from tkinter import Tk, Frame, LabelFrame, Label

from gui.BrowserSelectionFrame import BrowserSelectionFrame
from gui.HealthMonitorFrame import HealthMonitorFrame
from gui.LoginFrame import LoginFrame
from gui.ProcessingFrame import ProcessingFrame
from gui.SurveyFrame import SurveyFrame
from gui.WaitingForQrFrame import WaitingForQrFrame
from utilities.JensenLogger import JensenLogger

from web.CoreDriver import CoreDriver


class Jensen(Tk):
    def __init__(self):
        super().__init__()
        self.main_container = Frame(self)
        self.main_container.pack(side='top', fill='both', expand=True)
        self.frames = {}
        self.driver = CoreDriver()

        # Add web driver executables to path
        driver_path = os.path.join(os.getcwd(), 'tools', 'win' if platform.system() == 'Windows' else 'mac')
        key = 'Path' if 'Path' in os.environ else 'PATH'
        current_path = os.environ[key]
        if driver_path not in current_path:
            os.environ[key] += os.pathsep + driver_path

        # Update permissions on the drivers
        os.chmod(os.path.join(driver_path, 'chromedriver' if platform.system() is not 'Windows' else 'chromedriver.exe')
                 , 0o777)
        os.chmod(os.path.join(driver_path, 'geckodriver' if platform.system() is not 'Windows' else 'geckodriver.exe')
                 , 0o777)

        for frame in (BrowserSelectionFrame, LoginFrame, ProcessingFrame, WaitingForQrFrame, SurveyFrame):
            frame_name = frame.__name__
            f = frame(parent=self.main_container, controller=self, width=50, driver=self.driver)
            self.frames[frame_name] = f
            f.grid(row=0, column=0, sticky='nsew')

        self.health_container = HealthMonitorFrame(self.main_container, 50)
        self.health_container.grid(row=50, column=0, sticky='ew', padx=5)

        # Setup the logger
        self.jensen_logger = JensenLogger.get_instance()
        self.jensen_logger.configure(self.health_container)

        self.show_frame('BrowserSelectionFrame')

    def show_frame(self, frame_name, **kwargs):
        frame = self.frames[frame_name]
        frame.tkraise()
        if isinstance(frame, ProcessingFrame):
            client_name = kwargs['client_name']
            form = kwargs['form_name']
            frame.prepare_for_processing(client_name, form)
        elif isinstance(frame, WaitingForQrFrame):
            thread = threading.Thread(target=frame.start_waiting_for_qr)
            thread.start()


if __name__ == '__main__':
    root = Jensen()
    root.geometry('400x600')
    root.mainloop()
