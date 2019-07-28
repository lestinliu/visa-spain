import pickle
from googleapiclient.discovery import build

from utils.google_sheet import GoogleSheets

gs = GoogleSheets()

with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)
service = build('drive', 'v3', credentials=creds)

results = service.files().list(fields="files(id, name)", q="mimeType='application/pdf'").execute()
items = results.get('files', [])
links = {}
for item in items:
    links[item["name"]] = '=HYPERLINK("https://docs.google.com/uc?export=download&id={}";"{}")'.format(item["id"], item["name"])

visa = gs.open_sheet(gs.authorize(), "Visa Spain", "visa")
for person in visa.get_all_records():
    reg_num = person["script_comment"]
    if reg_num and "pdf" not in reg_num and "{}.pdf".format(reg_num) in links:
        visa.update_acell("U{}".format(person["id"] + 1), links["{}.pdf".format(reg_num)])

