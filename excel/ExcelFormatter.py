import openpyxl


class ExcelFormatter:
    def __init__(self, exported_file_name):
        self.current_address = None
        self.processed_file_name = exported_file_name.split('.')[0] + '_Processed.xlsx'
        self.work_book = openpyxl.load_workbook(exported_file_name)
        self.work_sheet = self.work_book.get_sheet_by_name(exported_file_name.split('.')[0])

        # Tracking attributes
        self.current_row = 1
        self.max_rows = self.work_sheet.max_row
        self.contact_set_count = 0
        self.square_footage_column_count = 0
        self.actual_rent_column_idx = 3
        self.first_contact_column_idx = 5

        self.format_zip_codes()
        self.remove_space_and_sale_price_columns()
        self.add_rent_column()
        # TODO remove protected mode

    def get_next_address(self):
        self.current_row += 1
        if self.current_row > self.max_rows:
            return -1
        else:
            return self.work_sheet['A' + str(self.current_row)]

    def format_zip_codes(self):
        for i in range(2, self.max_rows+1):
            zip_code = self.work_sheet['B' + str(i)]
            zip_code = zip_code[:-4]
            self.work_sheet['B' + str(i)] = zip_code

    def remove_space_and_sale_price_columns(self):
        self.work_sheet.delete_cols(3, 5)

    def add_rent_column(self):
        self.work_sheet.insert_cols(3)



    def add_square_footage(self, square_footage=None):
        pass

    def add_rent(self, add_rent):
        pass

    def add_contacts(self, contacts=None):
        pass

    def save(self):
        self.work_book.save(self.processed_file_name)


class Contact:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
