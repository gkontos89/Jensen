DRILL_DOWN_CLASS_NAME = 'drilldown'


class ClientEntryElement:
    def __init__(self, client_entry_element):
        self.client_entry_element = client_entry_element
        self.drill_down_element = self.client_entry_element.find_element_by_class_name(DRILL_DOWN_CLASS_NAME)

    def expand_plus_sign(self):
        # TODO figure this damn this out
        pass
