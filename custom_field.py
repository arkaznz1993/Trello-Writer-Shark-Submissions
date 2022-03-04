class CustomField:
    all_custom_fields = []

    def __init__(self, id, id_board, name, type):
        self.id = id
        self.id_board = id_board
        self.name = name
        self.type = type
        CustomField.all_custom_fields.append(self)

    def __repr__(self):
        return f"CustomField('{self.id}', '{self.id_board}', '{self.name}', '{self.type}')"

    @staticmethod
    def instantiate_from_list(db_list):
        for row in db_list:
            CustomField(row[0], row[1], row[2], row[3])

    @staticmethod
    def get_custom_field_by_id(id):
        for custom_field in CustomField.all_custom_fields:
            if id == custom_field.id:
                return custom_field
