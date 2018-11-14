

class ClientEntry:
    def __init__(self, name):
        self.client_name = name
        self.forms = dict()
        self.plus_sign
        self.minus_sign


class SurveysDriver:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.client_entries = dict()
        self.active_client_entry = None
        # TODO take a snapshot of the number of TRs.  new TRs get assigned to clients

    def get_client_entry_names(self):
        pass
        # Get the Dark Rows and Light Rows into one list

    def expand_client_entry_and_get_forms(self, client_name):
        pass

    def select_client_entry_form(self):
        pass