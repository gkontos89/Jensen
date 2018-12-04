import platform
import subprocess
import threading
import time
from tkinter import Button, Label, Tk, LabelFrame

from gui.BaseFrame import BaseFrame
from gui.ProcessingProgressBar import ProcessingProgressBar


class ProcessingFrame(BaseFrame):
    def __init__(self, parent, controller, width, driver=None):
        super().__init__(parent, width)
        self.parent = parent
        self.controller = controller
        self.driver = driver
        self.current_client_name = None
        self.current_form_name = None
        self.number_of_listings_to_process = -1
        self.processing_status_frame = LabelFrame(self, text='Processing', width=50, pady=20)
        self.processing_progress_frame = LabelFrame(self, text='Overall Progress', width=50)
        self.client_name_text = Label(self.processing_status_frame, text='')
        self.form_name_text = Label(self.processing_status_frame, text='')
        self.start_processing_button = Button(self.processing_status_frame, text='Start Processing',
                                              command=self.start_processing)
        self.continue_export_button = Button(self.processing_status_frame, text='Click after export is complete...',
                                             command=self.continue_export_button_command)
        self.exporting_data_text = Label(self.processing_status_frame)
        self.number_of_listings_found_text = Label(self.processing_status_frame)
        self.processing_address_text = Label(self.processing_status_frame)
        self.pre_processed_data_complete_text = Label(self.processing_status_frame)
        self.square_footage_retrieved_text = Label(self.processing_status_frame)
        self.rent_range_retrieved_text = Label(self.processing_status_frame)
        self.contact_information_retrieved_text = Label(self.processing_status_frame)
        self.processed_listings_track_text = Label(self.processing_progress_frame)
        self.processing_progress_bar = ProcessingProgressBar(self.processing_progress_frame)
        self.processed_file_complete_text = Label(self.processing_progress_frame)
        self.cancel_button = Button(self, text='Cancel', command=self.cancel_button_command)
        self.finished_button = Button(self, text='Finished', command=self.finished_button_command)
        self.view_processed_file_button = Button(self, text='View processed file',
                                                 command=self.view_processed_file_button_command)

        self.client_name_text.pack()
        self.form_name_text.pack()
        self.start_processing_button.pack()
        self.continue_export_button.pack()
        self.exporting_data_text.pack()
        self.number_of_listings_found_text.pack()
        self.pre_processed_data_complete_text.pack()
        self.processing_address_text.pack()
        self.square_footage_retrieved_text.pack()
        self.rent_range_retrieved_text.pack()
        self.contact_information_retrieved_text.pack()
        self.processed_listings_track_text.pack()
        self.processing_progress_bar.pack()
        self.processed_file_complete_text.pack()
        self.processing_status_frame.pack()
        self.processing_progress_frame.pack()
        self.cancel_button.pack()
        self.view_processed_file_button.pack()
        self.finished_button.pack()

    def prepare_for_processing(self, client_name, form):
        self.reset_processing_screen()
        self.current_client_name = client_name
        self.current_form_name = form
        self.client_name_text.config(text=self.current_client_name)
        self.form_name_text.config(text=self.current_form_name)
        self.start_processing_button.pack()

    def start_processing(self):
        self.start_processing_button.pack_forget()
        try:
            data_export_thread = threading.Thread(target=self.driver.initiate_data_export,
                                                  args=[self])
            data_export_thread.start()
        except:
            print('whoops')
            pass

    def reset_processing_screen(self):
        self.client_name_text.config(text='')
        self.form_name_text.config(text='')
        self.start_processing_button.pack_forget()
        self.continue_export_button.pack_forget()
        self.exporting_data_text.config(text='')
        self.number_of_listings_found_text.config(text='')
        self.pre_processed_data_complete_text.config(text='')
        self.processing_address_text.config(text='')
        self.square_footage_retrieved_text.config(text='')
        self.rent_range_retrieved_text.config(text='')
        self.contact_information_retrieved_text.config(text='')
        self.processed_listings_track_text.config(text='')
        self.processed_file_complete_text.config(text='')
        self.processing_progress_bar.reset()
        self.view_processed_file_button.pack_forget()
        self.finished_button.pack_forget()

    def update_name_of_processing_address(self, address_name):
        self.processing_address_text.config(text='Processing:  ' + address_name + ' ...')
        self.square_footage_retrieved_text.config(text='')
        self.rent_range_retrieved_text.config(text='')
        self.contact_information_retrieved_text.config(text='')
        self.processed_file_complete_text.config(text='')

    def set_number_of_processing_steps(self, number_of_processing_steps):
        self.processing_progress_bar.set_number_of_steps(number_of_processing_steps)

    def report_exporting_data_complete(self):
        self.processing_progress_bar.increment_step()
        self.exporting_data_text.config(text='Export from CoStar complete, processing...')

    def report_number_of_listings_found(self, number_of_listings):
        self.number_of_listings_to_process = number_of_listings
        self.number_of_listings_found_text.config(text=str(self.number_of_listings_to_process) + ' listings found...')
        self.processed_listings_track_text.config(text='0/' + str(self.number_of_listings_to_process)
                                                       + ' Listings processed...')

    def update_listings_processed(self, listings_processed):
        self.processed_listings_track_text.config(text=str(listings_processed) + '/' +
                                                  str(self.number_of_listings_to_process)
                                                  + ' Listings processed...')

    def report_pre_processed_data_complete(self):
        self.processing_progress_bar.increment_step()
        self.pre_processed_data_complete_text.config(text='Pre-process exported data complete...')

    def report_square_footage_retrieved(self):
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
        self.cancel_button.pack_forget()
        self.view_processed_file_button.pack()
        self.finished_button.pack()

    def show_continue_export_button(self):
        self.continue_export_button.pack()
        self.report_exporting_data_complete()

    def continue_export_button_command(self):
        process_client_thread = threading.Thread(target=self.driver.process_client_entry,
                                                 args=[self])
        process_client_thread.start()
        self.continue_export_button.pack_forget()

    def cancel_button_command(self):
        self.reset_processing_screen()
        self.controller.show_frame('SurveyFrame')
        pass

    def view_processed_file_button_command(self):
        processed_file_name = self.driver.get_processed_file_name()
        if platform.system() == 'Windows':
            subprocess.Popen('explorer "' + processed_file_name + '"')
            # TODO handle mac

    def finished_button_command(self):
        self.reset_processing_screen()
        self.controller.show_frame('SurveyFrame')


if __name__ == '__main__':
    root = Tk()
    root.geometry('500x500')
    pf = ProcessingFrame(root, root, 50)
    pf.continue_export_button.pack()
    pf.report_exporting_data_complete()
    pf.report_number_of_listings_found(25)
    pf.update_name_of_processing_address('my address')
    pf.set_number_of_processing_steps(10)

    pf.report_pre_processed_data_complete()
    pf.report_square_footage_retrieved()
    pf.report_rent_range_retrieved()
    pf.report_contact_information_retrieved()
    pf.report_address_processed()
    pf.report_processed_file_complete()
    pf.pack()
    root.mainloop()






