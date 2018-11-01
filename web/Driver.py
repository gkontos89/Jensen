import getpass
import os
import platform
from enum import Enum
from selenium import webdriver

from excel.ExcelProcessor import ExcelProcessor
from web.ExportDriver import ExportDriver
from web.element.LeaseDriver import LeaseDriver
from web.element.clients.AddressTableElement import AddressTableElement
from web.element.export.ExportFileTypeElement import ExportFileType
from web.element.clients.LeaseButtonElement import LeaseButtonElement
from web.element.login.LoginButtonElement import LoginButtonElement
from web.element.login.LoginElement import LoginElement
from web.element.clients.MenuElement import MenuElement
from web.element.clients.MySurveysIFrame import MySurveysIFrame
from web.element.login.PasswordElement import PasswordElement
from web.element.clients.SurveysElement import SurveysElement
from web.element.clients.TheClientListElement import TheClientListElement
from web.element.login.UsernameElement import UsernameElement


class WebBrowser(Enum):
    CHROME = 1
    FIREFOX = 2
    EDGE = 3


class Driver:
    def __init__(self):
        self.web_driver = None
        self.login_element = None
        self.login_button_element = None
        self.menu_element = None
        self.my_surveys_i_frame = None
        self.username_element = None
        self.password_element = None
        self.surveys_element = None
        self.the_client_list_element = None
        self.export_driver = None
        self.excel_processor = None

    def configure_web_driver(self, web_browser):
        # TODO add drivers to path
        if web_browser == WebBrowser.CHROME:
            self.web_driver = webdriver.Chrome()
        elif web_browser == WebBrowser.FIREFOX:
            self.web_driver = webdriver.Firefox()
        elif web_browser == WebBrowser.EDGE:
            self.web_driver = webdriver.Edge()

    def close_web_driver(self):
        self.web_driver.close()

    def go_to_costar(self):
        self.web_driver.get('http://costar.com')

    def go_to_login_screen(self):
        self.login_element = LoginElement(self.web_driver)
        self.login_element.go_to_login_screen()

    def enter_username(self, username):
        self.username_element = UsernameElement(self.web_driver)
        self.username_element.enter_username(username)

    def enter_password(self, password):
        self.password_element = PasswordElement(self.web_driver)
        self.password_element.enter_password(password)

    def press_login_button(self):
        self.login_button_element = LoginButtonElement(self.web_driver)
        self.login_button_element.login()

    def check_for_valid_credentials(self):
        self.web_driver.implicitly_wait(5)
        self.web_driver.find_element_by_class_name('instruction-message-container2')

    def enter_menu(self):
        self.menu_element = MenuElement(self.web_driver)
        self.menu_element.enter_menu()

    def go_to_surveys(self):
        self.surveys_element = SurveysElement(self.web_driver)
        self.surveys_element.go_to_surveys()

    def collect_surveys(self):
        self.my_surveys_i_frame = MySurveysIFrame(self.web_driver)
        self.web_driver.switch_to.frame(self.my_surveys_i_frame)
        self.the_client_list_element = TheClientListElement(self.web_driver)
        return self.the_client_list_element.get_all_client_entry_names()

    def expand_client_entry_and_get_forms(self, client_name):
        self.my_surveys_i_frame = MySurveysIFrame(self.web_driver)
        self.web_driver.switch_to.frame(self.my_surveys_i_frame)
        self.the_client_list_element = TheClientListElement(self.web_driver)
        client_entry_element = self.the_client_list_element.get_client_entry_element(client_name)
        # TODO expand the damn plus sign somehow and grab the forms with it
        return []

    def initiate_data_export(self, controller, export_file_type=ExportFileType.MICROSOFT_EXCEL_FILE):
        self.export_driver = ExportDriver(self.web_driver)
        self.export_driver.go_to_export_screen()
        self.export_driver.select_custom_export_filter('Retail 1')
        self.export_driver.select_export_file_type(export_file_type)
        self.export_driver.export_data()
        controller.show_continue_export_button()

    def process_client_entry(self, controller, client_name, form):
        """
        This will process a client's form all the way through exporting the data to csv, xls, ect. and then
        post processing the data into a properly formatted xlsx file

        :param controller: handle to frame that contains elements for updating a GUI for progress
        :param client_name:  name of the client as in the table
        :param form: the form entry created underneath the client name
        :return: N/A
        """
        # Process exported file
        self.excel_processor = ExcelProcessor()
        # Find out the file location based on OS
        download_path = None
        if platform.system() == 'Windows':
            download_path = os.path.join('C:\\Users', getpass.getuser(), 'Downloads', 'Export' + form + '.xls')
            # TODO figure out download location for MAC

        self.excel_processor.pre_process_file(download_path)  # TODO figure out extension
        controller.report_pre_processed_data_complete()

        '''
        +1 for exporting the excel sheet
        +1 for pre-processing export
        +1 for generating post processed excel sheet
        '''
        number_of_steps = len(self.excel_processor.address_entries) + 3
        controller.set_number_of_processing_steps(number_of_steps)

        # TODO loop through addresses and grab relevant information
        address_processed_count = 0
        total_addresses = len(self.excel_processor.address_entries)
        controller.report_number_of_listings_found(total_addresses)
        for address, address_entry in self.excel_processor.address_entries.items():
            controller.update_name_of_processing_address(address)

            # Grab the table and find the correct address link
            # Go to address page
            address_table_element = AddressTableElement(self.web_driver)
            address_table_element.go_to_address_entry(address)

            # Navigate to lease page
            lease_button_element = LeaseButtonElement(self.web_driver)
            lease_button_element.go_to_lease_info()
            lease_driver = LeaseDriver(self.web_driver)
            lease_driver.process_lease_listings(address_entry)
            controller.report_square_footage_retrieved()
            controller.report_rent_range_retrieved()
            controller.report_contact_information_retrieved()
            controller.report_address_processed()
            address_processed_count += 1
            controller.update_listings_processed(address_processed_count)

        self.excel_processor.generate_post_processed_file()
        controller.report_processed_file_complete()

        # TODO navigate back to Surveys option

    def get_processed_file_name(self):
        return self.excel_processor.processed_file_name

    def testing_only_quick_login(self):
        self.configure_web_driver(WebBrowser.FIREFOX)
        self.go_to_costar()
        self.go_to_login_screen()
        self.enter_username('sam.jensen@bairdwarner.com')
        self.enter_password('develop23')
        self.press_login_button()


if __name__ == '__main__':
    driver = Driver()
    driver.configure_web_driver(WebBrowser.FIREFOX)
    driver.go_to_costar()
    driver.go_to_login_screen()
    driver.enter_username('sam.jensen@bairdwarner.com')

    driver.press_login_button()
    # driver.enter_menu()
    # driver.go_to_surveys()
    # driver.process_client_entry('george', '10/18/2018')














