from googleapiclient.discovery import build
from google.oauth2 import service_account
import os.path
import re
import constants


def google_service(service_type):
    """Returns a Google service object based
    on the service_type parameter passed
    Currently creates Sheets, Docs, and Drive
    services.

    Args:
        service_type : Takes one of three values from the constants.py file

    Returns:
        A Google service object
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.environ.get('TRELLO_WRITER_SHARK_CLIENT_SECRET')):
        creds = service_account.Credentials.from_service_account_file(
            os.environ.get('TRELLO_WRITER_SHARK_CLIENT_SECRET'), scopes=constants.SCOPES)

    if service_type == constants.SHEETS:
        return build('sheets', 'v4', credentials=creds)
    elif service_type == constants.DOCS:
        return build('docs', 'v1', credentials=creds)
    else:
        return build('drive', 'v3', credentials=creds)


def get_id_from_url(url):
    doc_id = re.search('/[-\w]{25,}/', url).group()
    doc_id = doc_id.removeprefix('/')
    doc_id = doc_id.removesuffix('/')
    return doc_id
