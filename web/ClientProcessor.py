import threading
import time

from excel.ExcelProcessor import ExcelProcessor
from utilities.JensenLogger import JensenLogger
from web.AddressTableDriver import AddressTableDriver
from web.LeaseDriver import LeaseDriver


class ClientProcessor(threading.Thread):
    def __init__(self, core_driver, controller, client_name):
        super().__init__()
        self.stop_flag = threading.Event()
        self.core_driver = core_driver
        self.controller = controller
        self.client_name = client_name
        self.excel_processor = None

    def run(self):
        try:
            self.core_driver.export_driver.close_export_window()

            # Process exported file
            self.excel_processor = ExcelProcessor()
            self.excel_processor.pre_process_file(self.core_driver.export_driver.export_file_name, self.client_name)
            self.controller.report_pre_processed_data_complete()

            '''
            +1 for generating post processed excel sheet
            '''
            number_of_steps = len(self.excel_processor.address_entries) + 1
            self.controller.set_number_of_processing_steps(number_of_steps)
            address_processed_count = 0
            total_addresses = len(self.excel_processor.address_entries)
            self.controller.report_number_of_listings_found(total_addresses)
            for address, address_entry in self.excel_processor.address_entries.items():
                if not self.stop_flag.is_set():
                    self.controller.update_name_of_processing_address(address)

                    # Grab the table and find the correct address link
                    # Go to address page
                    address_table_driver = AddressTableDriver(self.core_driver.web_driver)
                    address_table_driver.select_list_view()
                    address_table_driver.go_to_address_page(address)

                    # Navigate to lease page and process listings
                    # TODO properly handle residential units
                    lease_driver = LeaseDriver(self.core_driver.web_driver)
                    leases_found = True
                    try:
                        # todo check what type of property it is to see if lease button or residential should be checked
                        lease_driver.go_to_lease_info()
                        JensenLogger.get_instance().log_info("Lease button clicked for address: " +
                                                             address_entry.address)
                    except:
                        JensenLogger.get_instance().log_exception("Potential no leases found for address: " +
                                                                  address_entry.address)
                        leases_found = False
                        pass

                    if leases_found:
                        JensenLogger.get_instance().log_info("Going to Leases for " + address_entry.address)
                        lease_driver.process_lease_listings(address_entry)

                    self.controller.report_square_footage_retrieved()
                    self.controller.report_rent_range_retrieved()
                    self.controller.report_contact_information_retrieved()
                    self.controller.report_address_processed()
                    address_processed_count += 1
                    self.controller.update_listings_processed(address_processed_count)

                    # Navigate back to address listings
                    back_link = self.core_driver.web_driver.find_element_by_class_name('masthead-back-link')
                    back_link.click()
        except:
            JensenLogger.get_instance().log_exception("Failed processing client!")

        try:
            self.excel_processor.generate_post_processed_file()
            self.controller.report_processed_file_complete()
        except:
            JensenLogger.get_instance().log_exception("Failed generating post processed excel file!")

        time.sleep(1)
        self.core_driver.open_menu()
        self.core_driver.go_to_surveys()
