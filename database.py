import os
import mysql.connector
from mysql.connector.constants import ClientFlag

# Instance name - flash-hour-338103:asia-south1:test-sql-server

config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': '35.200.140.194',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': os.environ.get('SSL_CA'),
    'ssl_cert': os.environ.get('SSL_CERT'),
    'ssl_key': os.environ.get('SSL_KEY'),
    'database': os.environ.get('DB_NAME'),
}

GET_WORDCOUNT = 'SELECT WordCount FROM CardDetails WHERE CardId = %s;'

GET_PROOFREADERS = 'SELECT TrelloId, Name FROM Writers'

GET_CUSTOM_FIELDS = 'SELECT * FROM CustomFields;'

GET_CUSTOM_FIELD_OPTIONS = 'SELECT CustomFieldOptions.* FROM CustomFieldOptions ' \
                           'JOIN CustomFields ON CustomFieldOptions.IdCustomField = CustomFields.Id;'

UPDATE_CARD = 'UPDATE CardDetails ' \
              'SET ' \
              'Penalty = %s,' \
              'Proofreader = %s,' \
              'ProofreaderName = %s,' \
              'CompletedDate = %s,' \
              'FinalDocLink = %s,' \
              'Rating = %s,' \
              'Status = %s ' \
              'WHERE ' \
              'CardId = %s;'


class DatabaseConnector:
    def __init__(self):
        self.connection = mysql.connector.connect(**config)
        self.cursor = self.connection.cursor()

    def get_word_count(self, id):
        self.cursor.execute(GET_WORDCOUNT, id)
        return self.cursor.fetchone()

    def get_proofreaders(self):
        self.cursor.execute(GET_PROOFREADERS)
        return self.cursor.fetchall()

    def get_custom_fields(self):
        self.cursor.execute(GET_CUSTOM_FIELDS)
        return self.cursor.fetchall()

    def get_custom_field_options(self):
        self.cursor.execute(GET_CUSTOM_FIELD_OPTIONS)
        return self.cursor.fetchall()

    def update_card_details(self, values):
        self.cursor.executemany(UPDATE_CARD, values)
        self.connection.commit()


database_connection = DatabaseConnector()
