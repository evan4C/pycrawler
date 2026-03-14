import argparse
from pathlib import Path
import redbook

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

    args = parser.parse_args()

    if args.mode == "redbook":
        redbook.extract_redbook(args.html)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
