from enum import Enum

from selenium.webdriver.support.select import Select

EXPORT_FILE_TYPE_ID = 'htmlExportFileType'


class ExportFileType(Enum):
    COMMA_SEPARATE_VALUES = 1
    MICROSOFT_EXCEL_FILE = 2


class ExportFileTypeElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = Select(self.web_driver_handle.find_element_by_id(EXPORT_FILE_TYPE_ID))

    def select_export_file_type(self, file_type):
        if file_type == ExportFileType.COMMA_SEPARATE_VALUES:
            self.web_element.select_by_visible_text('Comma Separated Values')
        elif file_type == ExportFileType.MICROSOFT_EXCEL_FILE:
            self.web_element.select_by_visible_text('Microsoft Excel File')

