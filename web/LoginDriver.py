from selenium.webdriver.common.keys import Keys


class LoginDriver:
    def __init__(self, driver):
        self.driver = driver

    def go_to_login_screen(self):
        """
        Navigates to the login screen
        :return:
        """
        go_to_login_element = self.driver.web_driver.find_element_by_link_text('Login')
        go_to_login_element.click()

    def login(self, username, password):
        """
        Logs into the application using passed in credentials
        :param username:
        :param password:
        :return:
        """
        username_element = self.driver.web_driver.find_element_by_id('username')
        password_element = self.driver.web_driver.find_element_by_id('password')
        login_button_element = self.driver.web_driver.find_element_by_id('loginButton')

        username_element.send_keys(Keys.CONTROL + 'a')
        username_element.send_keys(Keys.DELETE)
        username_element.send_keys(username)

        password_element.send_keys(Keys.CONTROL + 'a')
        password_element.send_keys(Keys.DELETE)
        password_element.send_keys(password)

        login_button_element.click()

    def check_for_valid_credentials(self):
        """
        Throws error if it cannot find the prompt to accept the code on the cell phone.  Those calling this function
        should be ready to handle the error
        :return: throws error
        """
        # TODO move this wait to the setup
        self.driver.web_driver.implicitly_wait(10)
        self.driver.web_driver.find_element_by_class_name('instruction-message-container2')
