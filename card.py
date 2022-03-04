from datetime import datetime
from pytz import timezone
import requests
import constants
from custom_field import CustomField
from custom_field_options import CustomFieldOption
from docs import Docs
from google_service import get_id_from_url
from proofreader import Proofreader

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
        self.proofreader = None
        self.proofreader_name = None
        self.word_count = None
        self.surfer_seo = ''
        self.doc_file_original = ''
        self.completed_date = None
        self.doc_file_copy2 = None
        self.wordcount_proofread = 0
        self.grammatical_errors = 0
        self.formatting_errors = 0
        self.continuity_errors = 0
        self.misc_errors = 0
        self.total_errors_per_500_words = 0
        self.instructions_followed = 'Yes'
        self.score = 80
        self.status = STATUS_COMPLETED
        self.remarks = 'None'

        try:
            if self.id_board == constants.BOARD_ID_EDITOR_ALPHA:
                print('Team Alpha')
            elif self.id_board == constants.BOARD_ID_EDITOR_BETA:
                print('Team Beta')
            elif self.id_board == constants.BOARD_ID_EDITOR_GAMMA:
                print('Team Gamma')

            self.set_card_proofreader()
            self.set_card_custom_fields()
            self.compute_score()
            self.get_card_doc_link()

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
        except:
            pass

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
                if c_field.name == 'Grammatical Errors':
                    self.grammatical_errors = int(custom_field_json['value']['number'])
                elif c_field.name == 'Formatting Errors':
                    self.formatting_errors = int(custom_field_json['value']['number'])
                elif c_field.name == 'Continuity Errors':
                    self.continuity_errors = int(custom_field_json['value']['number'])
                elif c_field.name == 'Misc Errors':
                    self.misc_errors = int(custom_field_json['value']['number'])
                elif c_field.name == 'Word Count Proofread':
                    self.wordcount_proofread = int(custom_field_json['value']['number'])
                elif c_field.name == 'Surfer SEO':
                    self.surfer_seo = custom_field_json['value']['text']
                elif c_field.name == 'Client ID':
                    self.client = custom_field_json['value']['number']
                elif c_field.name == 'Remarks':
                    self.remarks = custom_field_json['value']['text']
                elif c_field.name == 'Instructions Followed':
                    cfo = CustomFieldOption.get_custom_field_option_by_id(custom_field_json['idValue'])
                    self.instructions_followed = cfo.field_value

    def compute_score(self):
        self.deduct_for_each_error()

        if self.instructions_followed == 'Yes':
            self.score += 20

        if round(self.total_errors_per_500_words) > 5:
            print('TERRIBLEEEEE')

        print(f'FINAL SCORE: {self.score}')

    def deduct_for_each_error(self):
        errors = [self.grammatical_errors, self.formatting_errors, self.continuity_errors, self.misc_errors]

        for error in errors:
            error_per_500_words = round((500 / self.wordcount_proofread) * error)
            self.total_errors_per_500_words += (500 / self.wordcount_proofread) * error

            if error_per_500_words >= 4:
                self.score -= 16
            elif error_per_500_words == 3:
                self.score -= 10
            elif error_per_500_words == 2:
                self.score -= 4
            elif error_per_500_words == 1:
                self.score -= 2

    def get_card_doc_link(self):
        actions_url = URL + f'/{self.id}/actions'
        params = constants.PARAMS.copy()
        params["filter"] = "commentCard"
        response = requests.request(
            "GET",
            actions_url,
            params=params,
            headers=constants.HEADERS
        )
        doc_link = ''
        for comment_json in response.json():
            try:
                comment_text = comment_json['data']['text']
                if comment_text.startswith('https://docs.google.com/document/d/'):
                    doc_link = comment_text
            except:
                print('Ran into an error.')

        if len(doc_link) > 0:
            self.doc_file_original = doc_link
        else:
            self.doc_file_original = self.surfer_seo

    def convert_to_tuple_submissions(self):
        return tuple([self.proofreader, self.proofreader_name, self.completed_date, self.doc_file_copy2,
                      self.wordcount_proofread, self.grammatical_errors, self.formatting_errors,
                      self.continuity_errors, self.misc_errors, self.score, self.status, self.remarks, self.id])

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
