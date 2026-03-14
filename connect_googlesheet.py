from google.oauth2.service_account import Credentials
import gspread

from datetime import datetime
from redbook import RedbookNote

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def append_to_sheet(note: RedbookNote, spreadsheet_id: str, creds_path: str) -> None:
    """Append a redbook note to a google sheet"""
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    values = [timestamp, note.title, note.content, note.likes, note.collects, note.comments]
    sheet.append_row(values)
    print("append to google sheet successfully")
