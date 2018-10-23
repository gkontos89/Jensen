LINK_TEXT = 'Login'


class LoginElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_link_text(LINK_TEXT)

    def go_to_login_screen(self):
        self.web_element.click()
