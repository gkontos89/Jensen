from tkinter import Tk
from tkinter.ttk import Progressbar


class ProcessingProgressBar(Progressbar):
    def __init__(self, parent):
        super().__init__(parent)
        self.config(mode='determinate')
        self.max_step_units = 100
        self.current_step = 0
        self.number_of_steps = 0
        self.step_increment_amount = 0

    def set_number_of_steps(self, number_of_steps):
        self.config(value=0)
        self.current_step = 0
        self.number_of_steps = number_of_steps
        self.step_increment_amount = self.max_step_units / self.number_of_steps

    def increment_step(self):
        self.current_step += self.step_increment_amount
        if not self.current_step >= self.max_step_units:
            super().step(self.step_increment_amount)
        else:
            self.config(value=99.9)


if __name__ == '__main__':
    root = Tk()
    p = ProcessingProgressBar(root)
    p.pack()
    root.mainloop()


