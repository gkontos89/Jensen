import os
from tkinter import LabelFrame, Label, PhotoImage, LEFT, RIGHT


class HealthMonitorFrame(LabelFrame):
    def __init__(self, parent, width):
        super().__init__(parent)
        self.config(width=width)
        self.config(padx=60)
        self.config(text='Health Monitor')
        self.status_text = Label(self, text='Jensen is healthy')
        this_directory = os.path.dirname(__file__)
        check_path = os.path.join(this_directory, '../img/healthy.png')
        x_path = os.path.join(this_directory, '../img/unhealthy.png')
        self.healthy_image = PhotoImage(file=check_path)
        self.unhealthy_image = PhotoImage(file=x_path)
        self.status_image = Label(self, image=self.healthy_image)

        self.status_text.pack(side=LEFT)
        self.status_image.pack(side=RIGHT)

    def report_failure_occurred(self, msg=None):
        self.status_text.config(text='Error has occurred, please check logs' if msg is None else msg)
        self.status_image.config(image=self.unhealthy_image)

    def set_healthy_status(self):
        self.status_text.config(text='Jensen is healthy')
        self.status_image.config(image=self.healthy_image)



