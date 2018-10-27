MENU_ID = 'csgp-menu-label'


class MenuElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(MENU_ID)

    def enter_menu(self):
        self.web_element.click()
