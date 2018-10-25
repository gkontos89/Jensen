from enum import Enum
from selenium import webdriver

from excel.ExcelProcessor import ExcelProcessor
from web.element.ExportElement import ExportElement
from web.element.LoginButtonElement import LoginButtonElement
from web.element.LoginElement import LoginElement
from web.element.MenuElement import MenuElement
from web.element.MySurveysIFrame import MySurveysIFrame
from web.element.PasswordElement import PasswordElement
from web.element.SurveysElement import SurveysElement
from web.element.TheClientListElement import TheClientListElement
from web.element.UsernameElement import UsernameElement


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
        self.export_element = None
        self.excel_processor = None

    def configure_web_driver(self, web_browser):
        # TODO add drivers to path
        if web_browser == WebBrowser.CHROME:
            self.web_driver = webdriver.Chrome()
        elif web_browser == WebBrowser.FIREFOX:
            self.web_driver = webdriver.Firefox()
        elif web_browser == WebBrowser.EDGE:
            self.web_driver = webdriver.Edge()

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

    def process_client_entry(self, client_name, form):
        """
        This will process a client's form all the way through exporting the data to csv, xls, ect. and then
        post processing the data into a properly formatted xlsx file

        :param client_name:  name of the client as in the table
        :param form: the form entry created underneath the client name
        :return: N/A
        """
        self.my_surveys_i_frame = MySurveysIFrame(self.web_driver)
        self.web_driver.switch_to.frame(self.my_surveys_i_frame)
        self.the_client_list_element = TheClientListElement(self.web_driver)
        client_entry_element = self.the_client_list_element.get_client_entry_element(client_name)
        # TODO use this entry element to somehow expand the damn plus sign, then grab the correct form passed in

        # TODO actually use the export element
        self.export_element = ExportElement(self.web_driver)
        self.export_element.select_custom_filter()
        self.export_element.export_report() # TODO have argument for file extension?

        # Process exported file
        self.excel_processor = ExcelProcessor()
        self.excel_processor.pre_process_file(form)  # TODO figure out extension

        # TODO loop through addresses and grab relevant information
        for address, address_entry in self.excel_processor.address_entries.items():
            # TODO will this work? DO YOU HAVE TO SWITCH THE IFRAME BACK???
            self.go_to_surveys()

            # Go to address page

            # Go to lease page

            # Grab leases only for Relet, !Sublet, !Regus and get square footage options
            #address_entry.add_square_footage()

            # Grab rent range
            #address_entry.set_actual_rent()

            # Go to Individual Listing and grab contact information
            #address_entry.add_contact(name, email, phone)


        self.excel_processor.generate_post_processed_file()

        # TODO navigate back to Surveys option

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














