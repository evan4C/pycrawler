import argparse
from pathlib import Path
import redbook
from connect_googlesheet import append_to_sheet
from dotenv import load_dotenv
import os


def main():
    parser = argparse.ArgumentParser(
        prog="pycrawler",
        description="Web crawler with multiple extraction modes"
    )
    subparsers = parser.add_subparsers(dest="mode", help="Extraction mode")

    # redbook
    redbook_parser = subparsers.add_parser(
        "redbook",
        help="Extract info from redbook note html"
    )
    redbook_parser.add_argument(
        "html",
        type=Path,
        help="Path to the html file to extract info from"
    )
    redbook_parser.add_argument(
        "--sheet",
        type=str,
        help="Google sheet id to append extracted data to"
    )
    redbook_parser.add_argument(
        "--credentials",
        type=Path,
        help="Path to google oauth credentials file"
    )

    args = parser.parse_args()
    load_dotenv()

    if args.mode == "redbook":
        note = redbook.extract_redbook(args.html)
        if args.sheet:
            sheet_id = args.sheet
        else:
            sheet_id = os.getenv("SHEET_ID")
        
        if args.credentials:
            creds_path = args.credentials
        else:
            creds_path = os.getenv("GOOGLE_SHEET_CRED")

        append_to_sheet(note, sheet_id, creds_path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
