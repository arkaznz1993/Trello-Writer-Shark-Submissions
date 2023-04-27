import requests
import constants
from custom_field import CustomField
from custom_field_options import CustomFieldOption
from card import Card
from google_service import google_service
from database import database_connection
import time
from proofreader import Proofreader


def main(data, context):
    time_start = time.time()

    Card.docs_service = google_service(constants.DOCS)
    Card.drive_service = google_service(constants.DRIVE)
    Proofreader.instantiate_from_db_list(database_connection.get_proofreaders())
    CustomField.instantiate_from_list(database_connection.get_custom_fields())
    CustomFieldOption.instantiate_from_list(database_connection.get_custom_field_options())

    for list_id in constants.SUBMISSION_LIST_IDS:
        url = f"https://api.trello.com/1/lists/{list_id}/cards"

        response = requests.request(
            "GET",
            url,
            params=constants.PARAMS,
            headers=constants.HEADERS
        )

        Card.instantiate_from_json(response.json())

    database_connection.update_card_details(Card.convert_all_to_db_list())
    database_connection.connection.close()

    Card.move_cards_to_limbo()

    time_end = time.time()
    print(f'Time taken for program: {int(time_end - time_start)} seconds.')


if __name__ == '__main__':
    main('', '')
