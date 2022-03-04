class Proofreader:
    all_proofreaders = []

    def __init__(self, trello_id: str, name: str):
        self.id = trello_id
        self.name = name

        Proofreader.all_proofreaders.append(self)

    @staticmethod
    def instantiate_from_db_list(db_rows):
        for row in db_rows:
            Proofreader(row[0], row[1])

    @staticmethod
    def find_proofreader(proofreader_id):
        for proofreader in Proofreader.all_proofreaders:
            if proofreader.id == proofreader_id:
                return proofreader

