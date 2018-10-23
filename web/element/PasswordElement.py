PASSWORD_ID = 'password'


class PasswordElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(PASSWORD_ID)

    def enter_password(self, password):
        self.web_element.send_keys(password)
