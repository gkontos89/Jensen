from time import sleep
from tkinter import Tk, HORIZONTAL, Button
from tkinter import ttk

class B(Button):
    def __init__(self, master, p_handle):
        super().__init__(master)
        self.p_handle = p_handle
        self.config(command=self.update)

    def update(self):
        self.p_handle.step(49)




if __name__ == '__main__':

    root = Tk()


    p = ttk.Progressbar(root, orient=HORIZONTAL, mode='determinate', length=200, maximum=50)
    p.pack()

    b = B(root, p)
    b.pack()



    root.mainloop()
