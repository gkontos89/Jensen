LEFT_MENU_ID = 'tdLeftMenu'
LEF_MENU_TABLE_CLASS_NAME = 'size2'


class ExportElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.left_menu = self.web_driver_handle.find_element_by_id(LEFT_MENU_ID)
        self.left_menu_table = self.left_menu.find_element_by_class_name('size2')
        self.menu_elements = self.left_menu_table.find_elements_by_tag_name('tr')
        self.export_element = None
        for element in self.menu_elements:
            if element.text == 'Export Data':
                self.export_element = element
                break

    def go_to_export_screen(self):
        self.export_element.click()


