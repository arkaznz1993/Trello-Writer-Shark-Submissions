from datetime import datetime

import constants
from google_service import google_service
from spreadsheets import Sheet

sheets_service = google_service(constants.SHEETS)
calendar_sheet = Sheet(sheets_service, '12o73YDTAuCeb2n-w_pwPfT-f5bDdu26G7eeRQC0dVlU')
get_holidays = calendar_sheet.get_values('Holidays!A2:A')


def is_holiday(date, holidays_list):
    if date.isoweekday() == 7:
        return True
    for hol in holidays_list:
        day = datetime.strptime(hol[0], '%Y-%m-%d')
        if day.year == date.year:
            if day.month == date.month:
                if day.day == date.day:
                    return True
    return False


holiday = is_holiday(datetime.now(), get_holidays)
