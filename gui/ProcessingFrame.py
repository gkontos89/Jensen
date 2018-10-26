from tkinter import Button, Label

from gui.BaseFrame import BaseFrame
from gui.ProcessingProgressBar import ProcessingProgressBar


class ProcessingFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.processing_address_text = Label(self)
        self.exporting_data_text = Label(self)
        self.pre_processed_data_complete_text = Label(self)
        self.square_footage_retrieved_text = Label(self)
        self.rent_range_retrieved_text = Label(self)
        self.contact_information_retrieved_text = Label(self)
        self.processed_file_complete_text = Label(self)
        self.processing_progress_bar = ProcessingProgressBar(self)
        self.processed_file_complete_text.pack()
        self.exporting_data_text.pack()
        self.pre_processed_data_complete_text.pack()
        self.square_footage_retrieved_text.pack()
        self.rent_range_retrieved_text.pack()
        self.contact_information_retrieved_text.pack()
        self.processed_file_complete_text.pack()
        self.processing_progress_bar.pack()
        # TODO cancel button, Complete button to go back to surveys screen

    def start_processing(self, client_name, form):
        self.driver.process_client_entry(self, client_name, form)

    def update_name_of_processing_address(self, address_name):
        self.processing_address_text.config(text='Processing ' + address_name + ' ...')
        self.square_footage_retrieved_text.config(text='')
        self.rent_range_retrieved_text.config(text='')
        self.contact_information_retrieved_text.config(text='')
        self.processed_file_complete_text.config(text='')
        pass

    def set_number_of_processing_steps(self, number_of_processing_steps):
        self.processing_progress_bar.set_number_of_steps(number_of_processing_steps)

    def report_exporting_data_complete(self):
        self.processing_progress_bar.increment_step()
        self.exporting_data_text.config(text='Exported data complete...')

    def report_pre_processed_data_complete(self):
        self.processing_progress_bar.increment_step()
        self.pre_processed_data_complete_text.config(text='Pre-process exported data complete...')

    def report_square_footage_retrieved(self):
        # TODO handle list
        self.square_footage_retrieved_text.config(text='Square footage retrieved...')

    def report_rent_range_retrieved(self):
        self.rent_range_retrieved_text.config(text='Rent retrieved...')

    def report_contact_information_retrieved(self):
        self.contact_information_retrieved_text.config(text='Contact information retrieved...')

    def report_address_processed(self):
        self.processing_progress_bar.increment_step()

    def report_processed_file_complete(self):
        self.processing_progress_bar.increment_step()
        self.processed_file_complete_text.config(text='Processed file complete!')
        # TODO make 'Done' button visible
        # TODO hide cancel button








