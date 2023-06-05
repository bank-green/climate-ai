from dotenv import load_dotenv
import sys
import argparse
import logging

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
logging.info("Starting program…")


from src.store import store
from src.vectorize import embed
from src.query import query


parser = argparse.ArgumentParser(
    prog="python cli.py",
    description="Import, OCR, and vectorize data sources for ClimateAI",
)


subparsers = parser.add_subparsers(required=True)

parser_store = subparsers.add_parser("store")
parser_store.add_argument("--file")
parser_store.add_argument("--name")
parser_store.add_argument("--bank")
parser_store.add_argument("--list", action="store_true")
parser_store.set_defaults(func=store)

parser_store = subparsers.add_parser("embed")
parser_store.add_argument("--name", required=True)
parser_store.add_argument("--bank", required=True)
parser_store.set_defaults(func=embed)

parser_store = subparsers.add_parser("query")
parser_store.add_argument("--bank", required=True)
parser_store.add_argument("--query", required=True)
parser_store.set_defaults(func=query)

args = parser.parse_args()

args.func(args)
logging.info("Done.")
