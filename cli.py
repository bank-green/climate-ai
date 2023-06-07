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


def cli_store(args):
    from src.store import store_and_embed, store, embed

    if args.no_embedding:
        store(args.document_name, args.bank, args.file)
    elif args.embedding_only:
        embed(args.document_name, args.bank)
    else:
        store_and_embed(args.document_name, args.bank, args.file)


def cli_query(args):
    from src.query import query_by_new_query, query_by_id, store_query

    if args.query_id:
        query_by_id(args.bank, args.query_id)
    elif args.store_only:
        store_query(args.bank, args.query)
    else:
        query_by_new_query(args.bank, args.query)


parser = argparse.ArgumentParser(
    prog="python cli.py",
    description="Import, OCR, and vectorize data sources for ClimateAI",
)
subparsers = parser.add_subparsers(required=True)

parser_store = subparsers.add_parser("store")
parser_store.add_argument("--file", type=argparse.FileType("r"))
parser_store.add_argument("--document-name", required=True)
parser_store.add_argument("--bank", required=True)

embedding_only_group = parser_store.add_mutually_exclusive_group()
embedding_only_group.add_argument(
    "--embedding-only", action="store_true", default=False
)
embedding_only_group.add_argument("--no-embedding", action="store_true", default=False)

parser_store.set_defaults(func=cli_store)

parser_query = subparsers.add_parser("query")
parser_query.add_argument("--bank", required=True)

query_group = parser_query.add_mutually_exclusive_group()
query_group.add_argument("--query")
query_group.add_argument("--query-id", type=int)
query_group.add_argument("--store-only", action="store_true", default=False)
parser_query.set_defaults(func=cli_query)

args = parser.parse_args()


args.func(args)

logging.info("Done.")
