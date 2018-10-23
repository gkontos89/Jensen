LOGIN_BUTTON_ID = 'loginButton'


class LoginButtonElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(LOGIN_BUTTON_ID)

    def login(self):
        self.web_element.click()
