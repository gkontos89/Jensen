import datetime
import getpass
import os
import platform
import sys
import time
from enum import Enum

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

from excel.ExcelProcessor import ExcelProcessor
from utilities.JensenLogger import JensenLogger
from web.AddressTableDriver import AddressTableDriver
from web.ExportDriver import ExportDriver, ExportFileType
from web.LeaseDriver import LeaseDriver
from web.LoginDriver import LoginDriver


class WebBrowser(Enum):
    CHROME = 1
    FIREFOX = 2
    EDGE = 3
    SAFARI = 4


class CoreDriver:
    def __init__(self):
        self.web_driver = None
        self.export_driver = None
        self.excel_processor = None

    def configure_web_driver(self, web_browser):
        if web_browser == WebBrowser.CHROME:
            # use the user options
            chrome_options = Options()
            chrome_user_path = None
            if platform.system() is not 'Windows':
                chrome_user_path = os.path.join('/users/', getpass.getuser(), 'Library',
                                                'Application', 'Support', 'Google', 'Chrome',
                                                'Default')
            else:
                chrome_user_path = os.path.join('C:\\Users', getpass.getuser(), 'AppData', 'Local',
                                                'Google', 'Chrome', 'User Data', 'Default')
            chrome_argument = "user-data-dir=" + chrome_user_path
            chrome_options.add_argument(chrome_argument)
            self.web_driver = webdriver.Chrome(chrome_options=chrome_options)
        elif web_browser == WebBrowser.FIREFOX:
            self.web_driver = webdriver.Firefox()
        elif web_browser == WebBrowser.EDGE:
            self.web_driver = webdriver.Edge()
        elif web_browser == WebBrowser.SAFARI:
            self.web_driver = webdriver.Safari()

    def close_web_driver(self):
        self.web_driver.close()

    def go_to_costar(self):
        self.web_driver.get('http://costar.com')

    def open_menu(self):
        menu_element = self.web_driver.find_element_by_id('csgp-menu-label')
        menu_element.click()

    def home_page_has_loaded(self):
        try:
            self.web_driver.find_element_by_id('csgp-menu-label')
            return True
        except NoSuchElementException:
            return False

    def go_to_surveys(self):
        surveys_element = self.web_driver.find_element_by_link_text('Surveys')
        surveys_element.click()

    def initiate_data_export(self, controller):
        self.export_driver = ExportDriver(self.web_driver)
        self.export_driver.go_to_export_screen()
        self.export_driver.select_custom_export_filter('Retail 1')
        self.export_driver.select_export_file_type(ExportFileType.MICROSOFT_EXCEL_FILE)
        self.export_driver.export_data()
        controller.show_continue_export_button()

    def process_client_entry(self, controller):
        """
        This will process a client's form all the way through exporting the data to csv, xls, ect. and then
        post processing the data into a properly formatted xlsx file

        :param controller: handle to frame that contains elements for updating a GUI for progress
        :return: N/A
        """
        # TODO pass in client name to pass into the pre_process_file function
        try:
            self.export_driver.close_export_window()

            # Process exported file
            self.excel_processor = ExcelProcessor()
            self.excel_processor.pre_process_file(self.export_driver.export_file_name)
            controller.report_pre_processed_data_complete()

            '''
            +1 for generating post processed excel sheet
            '''
            number_of_steps = len(self.excel_processor.address_entries) + 1
            controller.set_number_of_processing_steps(number_of_steps)
            address_processed_count = 0
            total_addresses = len(self.excel_processor.address_entries)
            controller.report_number_of_listings_found(total_addresses)
            for address, address_entry in self.excel_processor.address_entries.items():
                controller.update_name_of_processing_address(address)

                # Grab the table and find the correct address link
                # Go to address page
                address_table_driver = AddressTableDriver(self.web_driver)
                address_table_driver.select_list_view()
                address_table_driver.go_to_address_page(address)

                # Navigate to lease page and process listings
                # TODO properly handle residential units
                lease_driver = LeaseDriver(self.web_driver)
                leases_found = True
                try:
                    lease_driver.go_to_lease_info()
                    JensenLogger.get_instance().log_info("Lease button clicked for address: " + address_entry.address)
                except:
                    JensenLogger.get_instance().log_exception("Potential no leases found for address: " +
                                                              address_entry.address)
                    leases_found = False
                    pass

                if leases_found:
                    JensenLogger.get_instance().log_info("Going to Leases for " + address_entry.address)
                    lease_driver.process_lease_listings(address_entry)

                controller.report_square_footage_retrieved()
                controller.report_rent_range_retrieved()
                controller.report_contact_information_retrieved()
                controller.report_address_processed()
                address_processed_count += 1
                controller.update_listings_processed(address_processed_count)

                # Navigate back to address listings
                back_link = self.web_driver.find_element_by_class_name('masthead-back-link')
                back_link.click()
        except:
            JensenLogger.get_instance().log_exception("Failed processing client!")

        try:
            self.excel_processor.generate_post_processed_file()
            controller.report_processed_file_complete()
        except:
            JensenLogger.get_instance().log_exception("Failed generating post processed excel file!")

        time.sleep(1)
        self.open_menu()
        self.go_to_surveys()

    def get_processed_file_name(self):
        return self.excel_processor.processed_file_name

    def testing_only_quick_login(self):
        self.configure_web_driver(WebBrowser.FIREFOX)
        self.go_to_costar()
        login_driver = LoginDriver(self)
        login_driver.go_to_login_screen()
        login_driver.login('sam.jensen@bairdwarner.com', 'develop23')

    def testing_only_quick_login_chrome(self):
        self.configure_web_driver(WebBrowser.CHROME)
        self.go_to_costar()
        login_driver = LoginDriver(self)
        login_driver.go_to_login_screen()
        login_driver.login('sam.jensen@bairdwarner.com', 'develop23')


if __name__ == '__main__':
    driver = CoreDriver()
    driver.configure_web_driver(WebBrowser.FIREFOX)
    driver.go_to_costar()
    '''
    For testing in IDLE do the following:
    import os
    os.chdir("C:\\Jensen")
    from web.CoreDriver import CoreDriver
    cd = CoreDriver()
    cd.testing_only_quick_login()
    '''














