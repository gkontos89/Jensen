class LeaseButtonElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.tabs_block = self.web_driver_handle.find_element_by_id('htmlTabsBlock')
        self.tabs_table = self.tabs_block.find_element_by_class_name('fusion-tab-detail-container')
        self.tab_row = self.tabs_table.find_element_by_tag_name('tr')
        self.tabs = self.tab_row.find_elements_by_tag_name('td')
        self.lease_tab_element = self.tabs[1]

    def go_to_lease_info(self):
        self.lease_tab_element.click()