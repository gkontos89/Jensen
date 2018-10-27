from tkinter import Frame, Tk

from gui.JensenBanner import JensenBanner


class BaseFrame(Frame):
    def __init__(self, parent, width, height=None):
        super().__init__(parent)
        self.master = parent
        self.jensen_banner = JensenBanner(self, banner_width=width)
        self.jensen_banner.pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = BaseFrame(root, 50)
    base_frame.pack()
    root.mainloop()
