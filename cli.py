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

    if args.no_embeddings:
        store(args.document_name, args.bank, args.file)
    elif args.embeddings_only:
        embed(args.document_name, args.bank)
    else:
        store_and_embed(args.document_name, args.bank, args.file)


def cli_query(args):
    from src.query import query_by_new_question, query_by_id, store_question, search

    if args.question_id:
        query_by_id(args.bank, args.question_id)
    elif args.store_only:
        store_question(args.bank, args.question)
    elif args.chunks_only:
        chunks = search(args.bank, args.question)
        for chunk in chunks:
            print(f"{chunk}\n\n==========================\n")
    else:
        query_by_new_question(args.bank, args.question)


parser = argparse.ArgumentParser(
    prog="python cli.py",
    description="Import, OCR, and vectorize data sources for ClimateAI",
)
subparsers = parser.add_subparsers(required=True)

parser_store = subparsers.add_parser("store")
parser_store.add_argument("--file", type=argparse.FileType("r"))
parser_store.add_argument("--document-name", required=True)
parser_store.add_argument("--bank", required=True)

embeddings_only_group = parser_store.add_mutually_exclusive_group()
embeddings_only_group.add_argument(
    "--embeddings-only", action="store_true", default=False
)
embeddings_only_group.add_argument(
    "--no-embeddings", action="store_true", default=False
)

parser_store.set_defaults(func=cli_store)

parser_query = subparsers.add_parser("query")
parser_query.add_argument("--bank", required=True)

query_group = parser_query.add_mutually_exclusive_group()
query_group.add_argument("--question")
query_group.add_argument("--question-id", type=int)

store_chunks_only_group = parser_query.add_mutually_exclusive_group()
store_chunks_only_group.add_argument("--store-only", action="store_true", default=False)
store_chunks_only_group.add_argument(
    "--chunks-only", action="store_true", default=False
)
parser_query.set_defaults(func=cli_query)

args = parser.parse_args()
args.func(args)

logging.info("Done.")
