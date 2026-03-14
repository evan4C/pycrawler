from google.oauth2.service_account import Credentials
import gspread

from datetime import datetime
from redbook import RedbookNote

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def append_to_sheet(note: RedbookNote | list[RedbookNote], spreadsheet_id: str, creds_path: str) -> None:
    """Append redbook note to a google sheet"""
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(note, list):
        note_list = note
        new_rows = []
        for note in note_list:
            new_row = [timestamp, note.title, note.content, note.likes, note.collects, note.comments]
            new_rows.append(new_row)
        sheet.append_rows(new_rows)
    else:
        new_row = [timestamp, note.title, note.content, note.likes, note.collects, note.comments]
        sheet.append_row(new_row)
    print("append to google sheet successfully")
