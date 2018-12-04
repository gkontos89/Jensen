import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class LeaseDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle

    def get_web_driver_wait_handle(self, driver=None, element_type=By.ID, element_string=None, multiple=False):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        if not driver:
            driver = self.web_driver_handle

        if multiple:
            return WebDriverWait(driver=driver, timeout=15, ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.presence_of_all_elements_located((element_type, element_string)))
        else:
            return WebDriverWait(driver=driver, timeout=15, ignored_exceptions=ignored_exceptions)\
                .until(expected_conditions.presence_of_element_located((element_type, element_string)))

    def go_to_lease_info(self):
        lease_tab_element = self.web_driver_handle.find_element_by_link_text('Lease')
        lease_tab_element.click()

    def process_lease_listings(self, address_entry):
        """

        :param address_entry: reference to an AddressEntry type to add information to from the web page
        :return:
        """
        # grab number of listings in the window to keep index track
        availability_grid_section = self.web_driver_handle.find_element_by_id('contenttableavailabilityGrid')
        available_spaces = availability_grid_section.find_elements_by_xpath("//div[@class='']")
        available_space = available_spaces[0]
        available_space.click()

        # grab handles for navigation
        # next_lease_button = self.web_driver_handle.find_element_by_class_name('right')
        next_lease_button = self.get_web_driver_wait_handle(element_type=By.CLASS_NAME, element_string='right')
        # close_button = self.web_driver_handle.find_element_by_class_name('close close-icon')
        back_button = self.web_driver_handle.find_element_by_class_name('go-back')
        num_clicks = len(available_spaces) - 1  # take one out because the first one already appears
        for i in range(0, num_clicks):

            # lease_element = self.web_driver_handle.find_element_by_id('LeaseType')
            lease_element = self.get_web_driver_wait_handle(element_string='LeaseType')
            lease_text = lease_element.find_element_by_xpath("//span[@data-bind='textWithTitle: LeaseType']")
            if lease_text.text == 'Relet':
                # grab rent
                # rent = self.web_driver_handle.find_element_by_id('Rent_Display')
                rent = self.get_web_driver_wait_handle(element_string='Rent_Display')
                rent_text = rent.find_element_by_xpath("//span[@data-bind='textWithTitle: Rent.Display']")
                address_entry.set_actual_rent(rent_text)  # TODO find out if you need multiple rents

                # grab square
                square_footage = self.get_web_driver_wait_handle(element_string='AvailableArea')
                # square_footage = self.web_driver_handle.find_element_by_id('AvailableArea')
                square_footage_text = square_footage.find_element_by_xpath("//span[@data-bind='text: AvailableArea']")
                address_entry.add_square_footage(square_footage_text.text)

                # grab contacts
                contacts_container = self.get_web_driver_wait_handle(element_type=By.CLASS_NAME, element_string='contacts-container')
                # contacts_container = self.web_driver_handle.find_element_by_class_name('contacts-container')
                # contact_boxes = contacts_container.find_elements_by_xpath("//div[@class='contact-box']")
                contact_boxes = self.get_web_driver_wait_handle(driver=contacts_container, element_type=By.XPATH, element_string="//div[@class='contact-box']", multiple=True)
                for contact_box in contact_boxes:
                    name_element = self.get_web_driver_wait_handle(driver=contact_box, element_type=By.CLASS_NAME, element_string='contact-name')
                    name = name_element.text

                    # only grab mobile phone
                    phone = None
                    phone_numbers_container = contact_box.\
                        find_element_by_xpath("//div[@class='section contact-details']//div[@data-bind='foreach: "
                                              "PhoneNumbers.Items']")
                    phone_number_elements = phone_numbers_container.find_elements_by_tag_name('div')
                    for phone_number_element in phone_number_elements:
                        if phone_number_element.\
                                find_element_by_xpath("//span[@data-bind='textWithTitle: Desc']").text == '(m)':
                            phone = phone_number_element.\
                                find_element_by_xpath("//span[@data-bind='textWithTitle: Number']").text

                    email = contact_box.find_element_by_tag_name('a').text
                    address_entry.add_contact(name=name, email=email, phone=phone)

            next_lease_button.click()
            time.sleep(1)  # I hate doing this, but for some reason the lease page isn't appearing fast enough
            # Getting killed by stale elements:
            # https://stackoverflow.com/questions/27003423/python-selenium-stale-element-fix

        back_button.click()

