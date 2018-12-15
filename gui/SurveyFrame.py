from tkinter import Button, Listbox, Scrollbar, LEFT, Tk, Y, Frame

from gui.BaseFrame import BaseFrame
from web.SurveysDriver import SurveysDriver


class SurveyFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.surveys_driver = SurveysDriver(self.driver)
        self.client_list_frame = Frame(self)
        self.form_list_frame = Frame(self)
        self.processing_frame = Frame(self)
        self.collect_surveys_button = Button(self, text='Collect Surveys', command=self.collect_surveys_button_command)
        self.client_list_box = Listbox(self.client_list_frame, height=10, width=35, exportselection=False,
                                       selectmode='single')
        self.client_list_box.bind('<Double-Button-1>', self.on_client_selection)
        self.client_list_scrollbar = Scrollbar(self.client_list_frame, command=self.client_list_box.yview)
        self.client_list_box.config(yscrollcommand=self.client_list_scrollbar.set)
        self.forms_list_box = Listbox(self.form_list_frame, height=10, width=35, exportselection=False, selectmode='single')
        self.forms_list_scrollbar = Scrollbar(self.form_list_frame, command=self.forms_list_box.yview)
        self.process_form_button = Button(self.processing_frame, text='Continue',
                                          command=self.process_form_button_command)

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
        self.client_list_box.delete(0, 'end')
        self.forms_list_box.delete(0, 'end')
        self.surveys_driver.reset_driver()
        self.surveys_driver.attach_to_survey_page()
        client_entry_names = self.surveys_driver.get_client_entry_names()
        for client_entry_name in client_entry_names:
            self.client_list_box.insert('end', client_entry_name)

    def on_client_selection(self, evt):
        try:
            widget = evt.widget
            index = int(widget.curselection()[0])
            value = widget.get(index)
            self.forms_list_box.delete(0, 'end')
            forms = self.surveys_driver.expand_client_entry_and_get_forms(value)
            for form in forms:
                self.forms_list_box.insert('end', form)
        except:
            print('Client selection failed')

    def process_form_button_command(self):
        try:
            client_name = self.client_list_box.get(self.client_list_box.curselection()[0])
            form_name = self.forms_list_box.get(self.forms_list_box.curselection()[0])
            self.client_list_box.delete(0, 'end')
            self.forms_list_box.delete(0, 'end')
            if form_name is not None:
                self.surveys_driver.select_client_entry_form(form_name)
                self.controller.show_frame('ProcessingFrame', client_name=client_name, form_name=form_name)
        except:
            print('Process form failed')


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    # root.resizable(0, 0)

    base_frame = SurveyFrame(root, root, 50)
    base_frame.client_list_box.insert('end', 'hello')
    base_frame.client_list_box.insert('end', 'yay')
    base_frame.client_list_box.insert('end', 'bye')
    base_frame.pack()
    root.mainloop()
