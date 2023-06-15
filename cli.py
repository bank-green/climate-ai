from dotenv import load_dotenv
import sys
import argparse
import logging
import requests
import tempfile

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
logging.info("Starting program…")


def cli_store(args):
    from src.store import store_and_chunkify_and_embed, store, chunkify_and_embed

    if args.url:
        logging.info(f'Downloading from url "{args.url}"…')
        response = requests.get(args.url)
        response.raise_for_status()
        suffix = ".pdf" if args.url.endswith(".pdf") else ".html"
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(response.content)
        tmp.close()
        args.file = tmp.name

    if args.no_embeddings:
        store(args.document_name, args.bank, args.file)
    elif args.embeddings_only:
        chunkify_and_embed(args.document_name, args.bank)
    else:
        store_and_chunkify_and_embed(args.document_name, args.bank, args.file)


def cli_query(args):
    from src.query import query_by_id, store_question
    from src.database_adapter import get_questions_with_ids

    if args.list_questions:
        question_rows = get_questions_with_ids()
        for row in question_rows:
            print(f"ID: {row[0]}\nQUESTION: {row[1]}\n")
    elif args.question_id:
        query_by_id(args.bank, args.question_id, args.chunks_only)
    elif args.new_question:
        store_question(args.new_question)


parser = argparse.ArgumentParser(
    prog="python cli.py",
    description="Import, OCR, and vectorize data sources for ClimateAI",
)
subparsers = parser.add_subparsers(required=True)

parser_store = subparsers.add_parser("store")
file_or_url_group = parser_store.add_mutually_exclusive_group()
file_or_url_group.add_argument("--file")
file_or_url_group.add_argument("--url")
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
parser_query.add_argument("--bank")
parser_query.add_argument("--list-questions", action="store_true", default=False)
parser_query.add_argument("--chunks-only", action="store_true", default=False)

query_group = parser_query.add_mutually_exclusive_group()
query_group.add_argument("--new-question")
query_group.add_argument("--question-id", type=int)
parser_query.set_defaults(func=cli_query)

args = parser.parse_args()
args.func(args)

logging.info("Done.")
