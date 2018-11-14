from selenium.webdriver.common.keys import Keys

USERNAME_ID = 'username'
PASSWORD_ID = 'password'
LOGIN_BUTTON_ID = 'loginButton'
LOGIN_LINK_TEXT = 'Login'


class LoginDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle

    def go_to_login_screen(self):
        """
        Navigates to the login screen
        :return:
        """
        go_to_login_element = self.web_driver_handle.find_element_by_link_text(LOGIN_LINK_TEXT)
        go_to_login_element.click()

    def login(self, username, password):
        """
        Logs into the application using passed in credentials
        :param username:
        :param password:
        :return:
        """
        username_element = self.web_driver_handle.find_element_by_id(USERNAME_ID)
        password_element = self.web_driver_handle.find_element_by_id(PASSWORD_ID)
        login_button_element = self.web_driver_handle.find_element_by_id(LOGIN_BUTTON_ID)

        username_element.send_keys(Keys.CONTROL + 'a')
        username_element.send_keys(Keys.DELETE)
        username_element.send_keys(username)

        password_element.send_keys(Keys.CONTROL + 'a')
        password_element.send_keys(Keys.DELETE)
        password_element.send_keyws(password)

        login_button_element.click()

    def check_for_valid_credentials(self):
        """
        Throws error if it cannot find the prompt to accept the code on the cell phone.  Those calling this function
        should be ready to handle the error
        :return: throws error
        """
        self.web_driver_handle.implicitly_wait(5)
        self.web_driver_handle.find_element_by_class_name('instruction-message-container2')
