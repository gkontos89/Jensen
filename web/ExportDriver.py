from web.element.export.CustomExportLayoutElement import CustomExportLayoutElement
from web.element.export.ExportDataElement import ExportDataElement
from web.element.export.ExportElement import ExportElement
from web.element.export.ExportFileTypeElement import ExportFileTypeElement


class ExportDriver:
    # TODO clean up with new export elements
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.export_element = None
        self.custom_export_selector = None
        self.export_file_type_select = None
        self.export_data_element = None
        self.original_window_handle = self.web_driver_handle.current_window_handle

    def go_to_export_screen(self):
        self.export_element = ExportElement(self.web_driver_handle)
        self.export_element.go_to_export_screen()
        self.web_driver_handle.switch_to.window(self.web_driver_handle.window_handles[-1])

    def select_custom_export_filter(self, layout_text):
        self.custom_export_selector = CustomExportLayoutElement(self.web_driver_handle)
        self.custom_export_selector.select_export_layout(layout_text)

    def select_export_file_type(self, file_type):
        self.export_file_type_select = ExportFileTypeElement(self.web_driver_handle)
        self.export_file_type_select.select_export_file_type(file_type)

    def export_data(self):
        self.export_data_element = ExportDataElement(self.web_driver_handle)
        self.export_data_element.export_data()

    def reset_window_handles(self):
        self.web_driver_handle.close()
        self.web_driver_handle.switch_to.window(self.original_window_handle)
