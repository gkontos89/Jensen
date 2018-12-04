import time

from selenium.common.exceptions import NoSuchElementException


class AddressTableDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.address_table = None
        self.address_entries = None

    def select_list_view(self):
        select_list_view_element = self.web_driver_handle.find_element_by_xpath("//i[@data-action='select-list-view']")
        select_list_view_element.click()

    def attach_to_address_table(self):
        self.address_table = self.web_driver_handle.find_element_by_class_name('fixedDataTableLayout_rowsContainer')
        address_rows = self.address_table.find_elements_by_class_name('fixedDataTableRowLayout_rowWrapper')
        # Remove top row that comes with it for some reason
        address_rows = address_rows[1:]
        self.address_entries = {}
        for address_row in address_rows:
            address_link = address_row.find_element_by_tag_name('span')
            self.address_entries[address_link.text.lower()] = address_link

    def go_to_address_page(self, address):
        """
        This function will attempt to go to the address page by traversing the address table and also handling if the
        needed address is on a different page
        :param address: address page to go to
        :return:
        """
        address = address.lower()
        # Grab the pagination window if exists
        pagination_items = None
        try:
            pagination_panel = self.web_driver_handle.find_element_by_id('pagination')
            pagination_items = pagination_panel.find_elements_by_tag_name('div')
        except NoSuchElementException:
            pass

        search_complete = False
        while not search_complete:
            self.attach_to_address_table()
            if address not in self.address_entries:
                if not pagination_items or len(pagination_items) < 1:
                    raise Exception("Address:  " + address + " not found!!!")
                else:
                    next_pagination_button = pagination_items[-1]
                    if 'disabled' in next_pagination_button.get_attribute('class'):
                        # TODO report to controller somehow
                        raise Exception("Address:  " + address + " not found, after searching all pages!!!")
                    else:
                        next_pagination_button.click()
                        time.sleep(1)
            else:
                search_complete = True

        self.address_entries[address].click()

