from selenium.webdriver.common.keys import Keys

USERNAME_ID = 'username'


class UsernameElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = web_driver_handle.find_element_by_id(USERNAME_ID)

    def enter_username(self, username):
        self.web_element.send_keys(Keys.CONTROL + 'a')
        self.web_element.send_keys(Keys.DELETE)
        self.web_element.send_keys(username)
