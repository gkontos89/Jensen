import time


class ClientEntry:
    def __init__(self, name, plus_sign, minus_sign):
        self.client_name = name
        self.forms = None
        self.plus_sign = plus_sign
        self.minus_sign = minus_sign

    def add_form_web_elements(self, form_web_elements):
        """
        Takes in a list of form web elements and stores in dictionary of link text and link web element
        :param form_web_elements: list of forms web elements
        :return:
        """
        self.forms = {}
        for form_web_element in form_web_elements:
            form_link = form_web_element.find_element_by_tag_name('a')
            self.forms[form_link.text] = form_link

    def get_form_names(self):
        return [key for key in self.forms]

    def expand_client_forms(self):
        self.plus_sign.click()

    def collapse_client_forms(self):
        self.minus_sign.click()

    def access_form(self, form_name):
        self.forms[form_name].click()


class SurveysDriver:
    def __init__(self, driver):
        self.driver = driver
        self.client_entries = dict()
        self.active_client_entry = None
        self.base_tr_snapshot = None
        self.surveyIFrame = None
        self.client_list_element = None
        self.client_list_body_element = None

    def reset_driver(self):
        self.client_entries = dict()
        self.active_client_entry = None
        self.base_tr_snapshot = None
        self.surveyIFrame = None
        self.client_list_element = None
        self.client_list_body_element = None

    def attach_to_survey_page(self):
        """
        Grabs the handle to the survey web element and scans in all the client entry names and stores handles to each.
        Gets a snap shot of the number of rows for tracking new rows added/removed when client names are expanded
        :return:
        """
        # Attach to web elements
        self.surveyIFrame = self.driver.web_driver.find_element_by_id('htmlMySurveysIFrame')
        self.driver.web_driver.switch_to.frame(self.surveyIFrame)
        self.client_list_element = self.driver.web_driver.find_element_by_id('theClientList')
        self.client_list_body_element = self.client_list_element.find_element_by_tag_name('tbody')

        # Take snap shot of the rows
        self.base_tr_snapshot = self.client_list_body_element.find_elements_by_tag_name('tr')

        # Process clients by grabbing dark and light rows separately, piecing them together in one list
        client_dark_rows = self.client_list_body_element.find_elements_by_class_name('RegularDarkRow')
        client_light_rows = self.client_list_body_element.find_elements_by_class_name('RegularLightRow')
        length = len(client_dark_rows) if len(client_dark_rows) > len(client_light_rows) else len(client_light_rows)
        client_rows = []
        for i in range(0, length):
            if i < len(client_dark_rows):
                client_rows.append(client_dark_rows[i])
            if i < len(client_light_rows):
                client_rows.append(client_light_rows[i])

        # Grab the plus and minus signs
        plus_signs = self.client_list_body_element.\
            find_elements_by_xpath("//img[@data-bind='visible: !displayRequirements() && numOfRequirements() > 0']")
        minus_signs = self.client_list_body_element.\
            find_elements_by_xpath("//img[@data-bind='visible: displayRequirements() && numOfRequirements() > 0']")

        # Create the client entries
        for i in range(0, len(client_rows)):
            client_name = client_rows[i].find_element_by_class_name('clientname').text
            self.client_entries[client_name] = ClientEntry(client_name, plus_signs[i], minus_signs[i])

    def get_client_entry_names(self):
        """
        returns all the clients names that are contained in the survey
        :return: list of client names
        """
        return [key for key in self.client_entries]

    def expand_client_entry_and_get_forms(self, client_name):
        """
        Expands the plus sign next to a client name to reveal the available forms.  The forms get stored in the client
        entry, contained in this driver.
        :param client_name:
        :return: list of forms
        """
        if self.active_client_entry is not None:
            try:
                self.active_client_entry.collapse_client_forms()
            except:
                pass  # TODO just pass for now, this could be if something does not get expanded

        client_entry = self.client_entries[client_name]
        client_entry.expand_client_forms()
        time.sleep(2)
        new_snap_shot_trs = self.client_list_body_element.find_elements_by_tag_name('tr')
        if client_entry.forms is None or len(client_entry.forms) == 0:
            client_entry.add_form_web_elements([row for row in new_snap_shot_trs if row not in self.base_tr_snapshot])

        self.base_tr_snapshot = self.base_tr_snapshot + \
            [row for row in new_snap_shot_trs if row not in self.base_tr_snapshot]
        self.active_client_entry = client_entry
        return client_entry.get_form_names()

    def select_client_entry_form(self, form_name):
        """
        Clicks the link to the specified form of the active client entry
        :param form_name:
        :return:
        """
        if self.active_client_entry is not None:
            self.active_client_entry.access_form(form_name)
            self.driver.web_driver.switch_to.default_content()

