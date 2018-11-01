class AddressTableElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.address_iframe = self.web_driver_handle.find_element_by_id('oGridFrame')
        self.web_driver_handle.switch_to.frame(self.address_iframe)
        self.address_table_element = web_driver_handle.find_element_by_xpath(
            "//div[@id='htmlFixedColumns']//table[@cellspacing='0']//table[@cellspacing='1']")
        self.address_entries_raw = self.address_table_element.find_elements_by_tag_name('tr')
        self.address_entries = {}
        for address_entry_raw in self.address_entries_raw:
            if address_entry_raw.text and address_entry_raw.text != 'Address':
                address_text = address_entry_raw.text.strip()
                self.address_entries[address_text] = address_entry_raw

    def go_to_address_entry(self, address):
        address_entry = self.address_entries[address]
        td_tags = address_entry.find_elements_by_tag_name('td')
        address_entry_link = td_tags[-1]
        address_entry_link.click()
        self.web_driver_handle.switch_to.default_content()
