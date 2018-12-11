import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from utilities.JensenLogger import JensenLogger


class LeaseDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle

    def get_web_driver_wait_handle(self, driver=None, element_type=By.ID, element_string=None, multiple=False, timeout=15):
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        if not driver:
            driver = self.web_driver_handle

        if multiple:
            return WebDriverWait(driver=driver, timeout=timeout, ignored_exceptions=ignored_exceptions) \
                .until(expected_conditions.presence_of_all_elements_located((element_type, element_string)))
        else:
            return WebDriverWait(driver=driver, timeout=timeout, ignored_exceptions=ignored_exceptions)\
                .until(expected_conditions.presence_of_element_located((element_type, element_string)))

    def go_to_lease_info(self):
        # lease_tab_element = self.web_driver_handle.find_element_by_link_text('Lease')
        lease_tab_element = self.get_web_driver_wait_handle(element_type=By.LINK_TEXT, element_string='Lease')
        lease_tab_element.click()

    def process_lease_listings(self, address_entry):
        """

        :param address_entry: reference to an AddressEntry type to add information to from the web page
        :return:
        """
        # grab number of listings in the window to keep index track
        # Sometimes leases don't load...
        # TODO handle "<div class="availability-spaces-not-available">No Spaces Available.</div>
        retries = 0
        availability_grid_section = None
        no_spaces_available = None
        while retries < 2:
            try:
                availability_grid_section = self.web_driver_handle.find_element_by_id('contenttableavailabilityGrid')
            except NoSuchElementException:
                try:
                    no_spaces_available = self.web_driver_handle.find_element_by_class_name('availability-spaces-not-available')
                except NoSuchElementException:






        retries = 0
        availability_grid_section = None
        while retries < 3:
            try:
                # Check to see if there are any leases even available
                try:
                    no_spaces_available = self.get_web_driver_wait_handle(element_type=By.CLASS_NAME,
                                                                          element_string='availability-spaces-not-available',
                                                                          timeout=2)
                    if no_spaces_available is not None:
                        JensenLogger.get_instance().log_info('No leases available for ' + address_entry.address)
                        address_entry.set_leasing_company_name('None')
                        return
                finally:
                    availability_grid_section = self.web_driver_handle.find_element_by_id('contenttableavailabilityGrid')
                    break
            except NoSuchElementException:
                self.web_driver_handle.refresh()
                retries += 1
                pass

        available_spaces = availability_grid_section.find_elements_by_xpath("//div[@class='']")
        available_space = available_spaces[0]
        available_space.click()

        # grab handles for navigation
        next_lease_button = None
        if len(available_spaces) > 1:
            # next_lease_button = self.web_driver_handle.find_element_by_class_name('right')
            next_lease_button = self.get_web_driver_wait_handle(element_type=By.CLASS_NAME, element_string='right')
            # close_button = self.web_driver_handle.find_element_by_class_name('close close-icon')

        back_button = self.web_driver_handle.find_element_by_class_name('go-back')
        num_clicks = len(available_spaces) - 1 if len(available_spaces) > 1 else 1  # take one out because the first one already appears
        for i in range(0, num_clicks):
            # lease_element = self.web_driver_handle.find_element_by_id('LeaseType')
            lease_element = self.get_web_driver_wait_handle(element_string='LeaseType')
            lease_text = lease_element.find_element_by_xpath("//span[@data-bind='textWithTitle: LeaseType']")
            if lease_text.text == 'Relet':
                # grab rent
                # rent = self.web_driver_handle.find_element_by_id('Rent_Display')
                rent = self.get_web_driver_wait_handle(element_string='Rent_Display')
                rent_text = rent.find_element_by_xpath("//span[@data-bind='textWithTitle: Rent.Display']")
                address_entry.set_actual_rent(rent_text.text)  # TODO find out if you need multiple rents

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

                    # Commented out is code that has issues with xpath.  This is the best way to do it but for now
                    # I can just grab the overall contact box text
                    contact_box_text_list = contact_box.text.split('\n')
                    phone = None
                    for string in contact_box_text_list:
                        if '(m)' in string:
                            phone = string
                    # phone_numbers_container = contact_box.\
                    #     find_element_by_xpath("//div[@class='section contact-details']//div[@data-bind='foreach: "
                    #                           "PhoneNumbers.Items']")
                    # phone_number_elements = phone_numbers_container.find_elements_by_tag_name('div')
                    # for phone_number_element in phone_number_elements:
                    #     if phone_number_element.\
                    #             find_element_by_xpath("//span[@data-bind='textWithTitle: Desc']").text == '(m)':
                    #         phone = phone_number_element.\
                    #             find_element_by_xpath("//span[@data-bind='textWithTitle: Number']").text

                    email_element = self.get_web_driver_wait_handle(driver=contact_box, element_type=By.TAG_NAME, element_string='a')
                    email = email_element.text
                    address_entry.add_contact(name=name, email=email, phone=phone)

            if next_lease_button:
                next_lease_button.click()

            time.sleep(1)  # I hate doing this, but for some reason the lease page isn't appearing fast enough
            # Getting killed by stale elements:
            # https://stackoverflow.com/questions/27003423/python-selenium-stale-element-fix

        back_button.click()

