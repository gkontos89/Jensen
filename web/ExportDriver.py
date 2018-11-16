from enum import Enum

from selenium.webdriver.support.select import Select


class ExportFileType(Enum):
    COMMA_SEPARATE_VALUES = 1
    MICROSOFT_EXCEL_FILE = 2


class ExportDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.export_file_type_extension = None

    def go_to_export_screen(self):
        more_menu_popup = self.web_driver_handle.find_element_by_id('more-menu-popup')
        export_button = more_menu_popup.find_element_by_xpath("//div[@data-action='export']")
        export_button.click()

    def select_custom_export_filter(self, layout_text):
        export_frame = self.web_driver_handle.find_element_by_name('export_frame')
        self.web_driver_handle.switch_to.frame(export_frame)
        custom_export_selector = Select(self.web_driver_handle.find_element_by_id('htmlExportLayout'))
        custom_export_selector.select_by_visible_text(layout_text)

    def select_export_file_type(self, file_type):
        export_file_type = Select(self.web_driver_handle.find_element_by_id('htmlExportFileType'))
        if file_type == ExportFileType.COMMA_SEPARATE_VALUES:
            export_file_type.select_by_visible_text('Comma Separated Values')
            self.export_file_type_extension = '.csv'
        elif file_type == ExportFileType.MICROSOFT_EXCEL_FILE:
            export_file_type.select_by_visible_text('Microsoft ExcelFile')
            self.export_file_type_extension = '.xls'

    def export_data(self):
        export_button = self.web_driver_handle.find_element_by_id('Button9')
        export_button.click()

    def close_export_window(self):
        self.web_driver_handle.switch_to.default_content()
        close_processing_window_button = self.web_driver_handle.find_element_by_class_name('close')
        close_processing_window_button.click()
