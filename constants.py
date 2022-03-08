import os

GOOGLE_DOC_LINK = 'https://docs.google.com/document/d/[DOC_ID]/edit'
USER_EMAIL = 'editor@writershark.com'

API_KEY = os.environ.get("TRELLO_API_KEY")
AUTH_TOKEN = os.environ.get("TRELLO_TOKEN")
PARAMS = {
    "key": API_KEY,
    "token": AUTH_TOKEN,
}
HEADERS = {
    "Accept": "application/json"
}

MAX_WORD_COUNT_PATTERN = '[0-9]{3,5} words'

SUBMISSION_LIST_IDS = ['619c718bd99d168d8bb7de7b', '61ed0fe6c075f7799d61f308', '6221bec01cf4f2072b5e4001']

BOARD_ID_EDITOR_ALPHA = '619c71771deda242e027685e'
BOARD_ID_EDITOR_BETA = '61ed0fd94bf5051e2602d02c'
BOARD_ID_EDITOR_GAMMA = '6221be34bd02aa64b89f82a2'


BOARD_ID_LIMBO = '61ed0d1760e6971c17cc623d'
LIST_ID_LIMBO = '61ed0e9f4676e32d3237ef91'

# Service type constants for Google Services
SHEETS = 1
DOCS = 2
DRIVE = 3

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/gmail.send']

# Date Time Related Things
DATE_FORMAT = '%Y-%m-%d'
