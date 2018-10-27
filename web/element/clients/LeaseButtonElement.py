class LeaseButtonElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = None

    def go_to_lease_info(self):
        self.web_element.click()