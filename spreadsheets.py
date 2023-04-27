class Sheet:
    """
    A class to interact with Google Sheets
    """

    def __init__(self, service: object, spreadsheet_id: str):
        """
        Args:
            service : Google Sheets service
            spreadsheet_id : The id of the spreadsheet
        """
        self.service = service
        self.spreadsheet_id = spreadsheet_id

    def get_values(self, spreadsheet_range: str):
        """Takes the spreadsheet range to return the values
        in the form of a list

        Args:
            spreadsheet_range : The spreadsheet range for which to obtain the values

        Returns:
            A list of rows which are also lists
        """
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id,
                                    range=spreadsheet_range).execute()
        return result.get('values', [])

    def clear_values(self, spreadsheet_range):
        self.service.spreadsheets().values().clear(
            spreadsheetId=self.spreadsheet_id,
            range=spreadsheet_range,
            body={}
        ).execute()

    def update_values(self, spreadsheet_range: str, values: list):
        """Takes the spreadsheet range to return the values
        in the form of a list

        Args:
            spreadsheet_range : The spreadsheet range for which to update the values
            values: This is the list of rows that needs to be updated
            in the specified range
        """
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=spreadsheet_range, body=body,
            valueInputOption='USER_ENTERED').execute()
        print(result.get('values', []))

    def append_values(self, spreadsheet_range: str, values: list):
        """Takes the spreadsheet range to return the values
        in the form of a list

        Args:
            spreadsheet_range : The spreadsheet range for which to append the values
            after the last row of the table
            values: This is the list of rows that needs to be appended
        """
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id, range=spreadsheet_range,
            valueInputOption='USER_ENTERED', body=body).execute()

        print('{0} cells appended.'.format(result \
                                           .get('updates') \
                                           .get('updatedCells')))
