class LeaseDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle

    def process_lease_listings(self, address_entry):
        """

        :param address_entry: reference to an AddressEntry type to add information to from the webpage
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
                address_entry.set_acutal_rent(rent_text)  # TODO find out if you need multiple rents

                # grab square
                square_footage = self.web_driver_handle.find_element_by_id('AvailableArea')
                square_footage_text = square_footage.find_element_by_xpath("//span[@data-bind='text: AvailableArea']")
                address_entry.add_square_footage(square_footage_text.text)

                # grab contacts
                contacts_container = self.web_driver_handle.find_element_by_class_name('contacts-container')
                contact_boxes = contacts_container.find_elements_by_xpath("//div[@class='contact-box']")
                for contact_box in contact_boxes:
                    name = contact_box.find_element_by_class_name("contact-name").text
                    phone = None
                    email = None
                    address_entry.add_contact(name=name, email=email, phone=phone)

            # TODO find special back button handle and click it