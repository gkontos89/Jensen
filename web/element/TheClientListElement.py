from .ClientEntryElement import ClientEntryElement

THE_CLIENT_LIST_ELEMENT_ID = 'theClientList'


class TheClientListElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(THE_CLIENT_LIST_ELEMENT_ID)

    def get_client_entry_element(self, client_name):
        client_entry_element = None
        table_row_elements = self.web_element.find_elements_by_tag_name('tr')
        for row_element in table_row_elements:
            client_name_element = row_element.find_element_by_class_name(client_name)
            if client_name == client_name_element.text:
                client_entry_element = row_element
                break

        return ClientEntryElement(client_entry_element)
