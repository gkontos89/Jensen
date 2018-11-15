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
        for address_row in address_rows:
            address_link = address_row.find_element_by_tag_name('span')
            self.address_entries[address_link.text] = address_link

    def go_to_address_page(self, address):
        self.address_entries[address].click()

