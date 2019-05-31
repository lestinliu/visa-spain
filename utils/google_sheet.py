import datetime
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from utils import config


class GoogleSheets:
    visa_columns = {
        "id": "A",
        "type": "B",
        "last_name": "C",
        "first_name": "D",
        "passport": "E",
        "birth_date": "F",
        "pasport_issued": "G",
        "passport_expired": "H",
        "issued_by": "I",
        "phone": "J",
        "nationality": "K",
        "travel_date": "L",
        "start_date": "M",
        "end_date": "N",
        "family": "O",
        "status": "P",
        "script_comment": "Q",
        "email": "R"
    }

    def authorize(self):
        """
        GS authorization
        """
        scope = config.GOOGLE_AUTH_SCOPES
        credentials = ServiceAccountCredentials.from_json_keyfile_name(config.GOOGLE_API_PROJECT, scope)
        google_sheet = gspread.authorize(credentials)
        return google_sheet

    def open_sheet(self, spread_sheet, name, worksheet):
        """
        Open google sheet
        Args:
            spread_sheet: Google App object.
            name: string, Google Sheet name.
            worksheet: string, list name
        """
        global temp_sh
        try:
            temp_sh = spread_sheet.open(name).worksheet(worksheet)
        except gspread.exceptions.SpreadsheetNotFound:
            print("ERROR:")
            print("---")
            print("Failed to open google sheet with name {0} and worksheet {1}".format(name, worksheet))
            print("Please, make sure if Google Sheet was shared with developer account from config")
            print("---")
            exit(-1)
        return temp_sh

    def filter_visa_with_appropriate_date(self, ls, date):
        input_dict = json.loads(ls)
        output_dict = [x for x in input_dict if datetime.datetime.strptime(x["start_date"], '%d/%m/%Y').date()
                       <= date
                       <= datetime.datetime.strptime(x["end_date"], '%d/%m/%Y').date() and not x["status"]]
        return output_dict

    def find_visa_item_by_id(self, spread_sheet, visa_item_id):
        cell = spread_sheet.row_values(visa_item_id + 1)
        return cell

    def update_visa_item_by_id(self, spread_sheet, id, column, value):
        spread_sheet.update_acell("{}{}".format(self.visa_columns[column], int(id) + 1), value)
