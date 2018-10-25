from tkinter import Button, Listbox, Scrollbar, VERTICAL, LEFT, Tk, Y, RIGHT, Frame

from gui.BaseFrame import BaseFrame


class SurveyFrame(BaseFrame):
    def __init__(self, parent, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.driver = driver
        self.client_list_frame = Frame(self)
        self.form_list_frame = Frame(self)
        self.processing_frame = Frame(self)
        self.collect_surveys_button = Button(self, text='Collect Surveys', command=self.collect_surveys_button_command)
        self.client_list_box = Listbox(self.client_list_frame, height=10, width=35)
        self.client_list_box.insert('end', 'hello')
        self.client_list_box.bind('<<ListboxSelect>>', self.on_client_selection)
        self.client_list_scrollbar = Scrollbar(self.client_list_frame, command=self.client_list_box.yview)
        self.client_list_box.config(yscrollcommand=self.client_list_scrollbar.set)
        self.forms_list_box = Listbox(self.form_list_frame, height=10, width=35)
        self.forms_list_scrollbar = Scrollbar(self.form_list_frame, command=self.forms_list_box.yview)
        self.process_form_button = Button(self.processing_frame, text='Process Form', command=self.process_form_button_command)

        # Packing
        self.collect_surveys_button.pack()
        self.client_list_box.pack(side=LEFT)
        self.client_list_scrollbar.pack(side=LEFT, fill=Y)
        self.client_list_frame.pack()
        self.forms_list_box.pack(side=LEFT)
        self.forms_list_scrollbar.pack(side=LEFT, fill=Y)
        self.form_list_frame.pack()
        self.process_form_button.pack()
        self.processing_frame.pack()

    def collect_surveys_button_command(self):
        client_entry_names = self.driver.collect_surveys()
        for client_entry_name in client_entry_names:
            self.client_list_box.insert('end', client_entry_name)

    def on_client_selection(self, evt):
        widget = evt.widget
        index = int(widget.curselection()[0])
        value = widget.get(index)
        self.driver.expand_client_entry(value)

    def process_form_button_command(self):
        # TODO implement controller, throw error for no selection
        client_name = self.client_list_box.get(self.client_list_box.curselection())
        form = self.forms_list_box.get(self.forms_list_box.curselection())
        self.driver.process_client_entry(client_name, form)


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = SurveyFrame(root, 50)
    base_frame.pack()
    root.mainloop()