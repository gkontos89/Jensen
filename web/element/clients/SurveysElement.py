SURVEYS_TEXT = 'Surveys'


class SurveysElement:
    def __init__(self, web_driver_handle):
        self.web_driver_handle = web_driver_handle
        self.web_element = self.web_driver_handle.find_element_by_link_text(SURVEYS_TEXT)

    def go_to_surveys(self):
        self.web_element.click()
