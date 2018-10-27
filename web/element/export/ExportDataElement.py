EXPORT_DATA_ID = 'Button9'


class ExportDataElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(EXPORT_DATA_ID)

    def export_data(self):
        self.web_element.click()
