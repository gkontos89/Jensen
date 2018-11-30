import time

from selenium.webdriver import ActionChains


class LeaseDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle

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
        for i in range(0, len(available_spaces)):
            temp_availability_grid_section = self.web_driver_handle.find_element_by_id('contenttableavailabilityGrid')
            temp_available_spaces = temp_availability_grid_section.find_elements_by_xpath("//div[@class='']")
            available_space = temp_available_spaces[i]
            available_space.click()

            lease_element = self.web_driver_handle.find_element_by_id('LeaseType')
            lease_text = lease_element.find_element_by_xpath("//span[@data-bind='textWithTitle: LeaseType']")
            if lease_text.text == 'Relet':
                # grab rent
                rent = self.web_driver_handle.find_element_by_id('Rent_Display')
                rent_text = rent.find_element_by_xpath("//span[@data-bind='textWithTitle: Rent.Display']")
                address_entry.set_actual_rent(rent_text)  # TODO find out if you need multiple rents

                # grab square
                square_footage = self.web_driver_handle.find_element_by_id('AvailableArea')
                square_footage_text = square_footage.find_element_by_xpath("//span[@data-bind='text: AvailableArea']")
                address_entry.add_square_footage(square_footage_text.text)

                # grab contacts
                contacts_container = self.web_driver_handle.find_element_by_class_name('contacts-container')
                contact_boxes = contacts_container.find_elements_by_xpath("//div[@class='contact-box']")
                for contact_box in contact_boxes:
                    name = contact_box.find_element_by_class_name("contact-name").text

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

            time.sleep(1)  # I hate doing this, but for some reason the lease page isn't appearing fast enough

            go_back_button = self.web_driver_handle.find_element_by_class_name('go-back')
            '''
            Attempt 1
            go_back_button.click()  # cannot be scrolled into view
            
            Attempt 2
            action = ActionChains(self.web_driver_handle)
            action.move_to_element(go_back_button).perform()  # rect is undefined
            action.click()
            
            Attempt 3
            action = ActionChains(self.web_driver_handle)
            action.move_to_element(go_back_button)
            action.click()
            action.perform()
            '''
            action = ActionChains(self.web_driver_handle)
            action.move_to_element(go_back_button)
            action.click()
            action.perform()
