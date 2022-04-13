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

    delegated_credentials = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')):
        creds = service_account.Credentials.from_service_account_file(
            os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'), scopes=constants.SCOPES)
        delegated_credentials = creds.with_subject(constants.USER_EMAIL)

    if service_type == constants.SHEETS:
        return build('sheets', 'v4', credentials=delegated_credentials)
    elif service_type == constants.DOCS:
        return build('docs', 'v1', credentials=delegated_credentials)
    else:
        return build('drive', 'v3', credentials=delegated_credentials)


def get_id_from_url(url):
    if url[-1] != '/':
        url = url + '/'
    doc_id = re.search('/[-\w]{25,}/', url).group()
    doc_id = doc_id.removeprefix('/')
    doc_id = doc_id.removesuffix('/')
    return doc_id
