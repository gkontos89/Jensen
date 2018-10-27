from selenium.webdriver.support.select import Select

CUSTOM_EXPORT_LAYOUT_ID = 'htmlExportLayout'


class CustomExportLayoutElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.custom_export_selector = Select(self.web_driver_handle.find_element_by_id(CUSTOM_EXPORT_LAYOUT_ID))

    def select_export_layout(self, layout_text):
        self.custom_export_selector.select_by_visible_text(layout_text)