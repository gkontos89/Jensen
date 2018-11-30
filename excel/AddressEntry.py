from excel.Contact import Contact


class AddressEntry:
    def __init__(self, address):
        self.address = address
        self.zip_code = None
        self.square_footage = []
        self.actual_rent = -1
        self.leasing_company_name = None
        self.contacts = []

    def set_zip_code(self, zip_code):
        self.zip_code = zip_code[:5]

    def set_actual_rent(self, actual_rent):
        self.actual_rent = actual_rent

    def add_contact(self, name, email, phone):
        self.contacts.append(Contact(name, email, phone))

    def add_square_footage(self, square_footage):
        self.square_footage.append(square_footage)

    def set_leasing_company_name(self, leasing_company_name):
        self.leasing_company_name = leasing_company_name
