from tkinter import Frame, Label, Tk, BOTH

from version import version


class JensenBanner(Frame):
    def __init__(self, parent, banner_width=25):
        super().__init__(parent)
        self.master = parent

        # Label
        self.label = Label(self)
        self.label.config(text='Jensen ' + version)
        self.label.config(bg='#000000')
        self.label.config(fg='#fff')
        self.label.config(width=banner_width)
        self.label.pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    jb = JensenBanner(root)
    jb.pack(fill=BOTH)
    root.mainloop()
