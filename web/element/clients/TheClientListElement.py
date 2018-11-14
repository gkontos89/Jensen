from .ClientEntryElement import ClientEntryElement

THE_CLIENT_LIST_ELEMENT_ID = 'theClientList'
CLIENT_NAME_CLASS_NAME = 'clientname'


class TheClientListElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_id(THE_CLIENT_LIST_ELEMENT_ID)

    def get_all_client_entry_names(self):
        client_entry_names = []
        table_row_elements = self.web_element.find_elements_by_tag_name('tr')  # TODO can't do this

        client_list_body = self.web_element.find_element_by_tag_name('tbody')
        client_rows = client_list_body.find_elements_by_class_name('RegularDarkRow') \
            + client_list_body.find_elements_by_class_name('RegularLightRow')
        for client_row in client_rows:
            client_name_element = client_row.find_element_by_class_name(CLIENT_NAME_CLASS_NAME)
            client_entry_names.append(client_name_element.text)

        return client_entry_names

    def get_client_entry_element(self, client_name):
        client_entry_element = None
        table_row_elements = self.web_element.find_elements_by_tag_name('tr')
        for row_element in table_row_elements:
            client_name_element = row_element.find_element_by_class_name(CLIENT_NAME_CLASS_NAME)
            if client_name == client_name_element.text:
                client_entry_element = row_element
                break

        return ClientEntryElement(client_entry_element)
