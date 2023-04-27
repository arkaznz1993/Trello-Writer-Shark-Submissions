from datetime import datetime
from pytz import timezone
import requests
import constants
from custom_field import CustomField
from custom_field_options import CustomFieldOption
from docs import Docs
from google_service import get_id_from_url
from proofreader import Proofreader
from database import database_connection

URL = "https://api.trello.com/1/cards"
STATUS_COMPLETED = 2


class Card:
    all_cards = []
    docs_service = None
    drive_service = None

    def __init__(self, id: str, title: str, url: str, id_list: str, id_board: str, desc: str):
        self.id = id
        self.title = title
        self.url = url
        self.id_list = id_list
        self.id_board = id_board
        self.desc = desc
        self.client = None
        self.penalty = 0
        self.proofreader = None
        self.proofreader_name = None
        self.word_count = None
        self.surfer_seo = ''
        self.doc_file_original = ''
        self.completed_date = None
        self.doc_file_copy2 = None
        self.rating = constants.RATING_AVERAGE
        self.instructions_followed = 'Yes'
        self.status = STATUS_COMPLETED

        try:
            self.set_card_proofreader()
            self.set_card_custom_fields()
            self.compute_penalty()
            self.set_card_doc_link()

            if self.doc_file_original.startswith('https://docs.google.com/document/d/'):
                doc_id = get_id_from_url(self.doc_file_original)
                doc_file = Docs(Card.docs_service, doc_id)

                copy_title = doc_file.title
                body = {
                    'name': copy_title
                }
                drive_response = Card.drive_service.files().copy(
                    fileId=doc_id, body=body).execute()
                document_copy_id = drive_response.get('id')
                self.doc_file_copy2 = constants.GOOGLE_DOC_LINK.replace('[DOC_ID]', document_copy_id)
            else:
                self.doc_file_copy2 = self.doc_file_original

            Card.all_cards.append(self)
        except Exception as e:
            print(e)

    def __repr__(self):
        return f"Card('{self.id}', '{self.title}', '{self.url}', '{self.id_list}', '{self.id_board}', '{self.desc}')"

    @staticmethod
    def instantiate_from_json(cards_json):
        for card_json in cards_json:
            Card(
                card_json['id'],
                card_json['name'],
                card_json['url'],
                card_json['idList'],
                card_json['idBoard'],
                card_json['desc']
            )

    def set_card_proofreader(self):
        actions_url = URL + f'/{self.id}/actions'
        params = constants.PARAMS.copy()
        params["filter"] = "addMemberToCard"
        response = requests.request(
            "GET",
            actions_url,
            params=params,
            headers=constants.HEADERS
        )

        card_members_json = response.json()
        self.proofreader = card_members_json[0]['data']['member']['id']
        proofreader_object = Proofreader.find_proofreader(self.proofreader)
        self.proofreader_name = proofreader_object.name

    def set_card_custom_fields(self):
        proofreading_field_url = URL + f'/{self.id}/customFieldItems'

        response = requests.request(
            "GET",
            proofreading_field_url,
            params=constants.PARAMS,
            headers=constants.HEADERS
        )

        now = datetime.now(timezone('Asia/Kolkata'))
        now = now.strftime('%Y-%m-%d %H:%M:%S')
        self.completed_date = now

        for custom_field_json in response.json():
            c_field = CustomField.get_custom_field_by_id(custom_field_json['idCustomField'])
            if c_field is not None:
                if c_field.name == 'Rating':
                    cfo = CustomFieldOption.get_custom_field_option_by_id(custom_field_json['idValue'])
                    self.rating = cfo.field_value
                elif c_field.name == 'Surfer SEO':
                    self.surfer_seo = custom_field_json['value']['text']
                elif c_field.name == 'Doc Link':
                    self.doc_file_original = custom_field_json['value']['text']
                    print('SUBMISSION DOC LINK IS: ' + self.doc_file_original)
                elif c_field.name == 'Client ID':
                    self.client = custom_field_json['value']['number']

    def compute_penalty(self):
        if self.rating == constants.RATING_POOR or self.rating == constants.RATING_BAD:
            word_count = database_connection.get_word_count([self.id])[0]
            if self.rating == constants.RATING_BAD:
                self.penalty = int(0.25 * word_count)
            else:
                self.penalty = int(0.5 * word_count)

            print(f'FINAL PENALTY: {self.penalty}')

    def set_card_doc_link(self):
        if len(self.surfer_seo) > 0:
            self.doc_file_original = self.surfer_seo

    def convert_to_tuple_submissions(self):
        return tuple([self.penalty, self.proofreader, self.proofreader_name, self.completed_date, self.doc_file_copy2,
                      self.rating, self.status, self.id])

    @staticmethod
    def convert_all_to_db_list():
        values = []
        for card in Card.all_cards:
            values.append(card.convert_to_tuple_submissions())

        return values

    @staticmethod
    def move_cards_to_limbo():
        for card in Card.all_cards:
            update_url = URL + f'/{card.id}/'
            params = constants.PARAMS.copy()
            params['idBoard'] = constants.BOARD_ID_LIMBO
            params['idList'] = constants.LIST_ID_LIMBO

            response = requests.request(
                "PUT",
                update_url,
                params=params,
                headers=constants.HEADERS
            )

            print(response.status_code)
