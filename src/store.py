import logging
from .database_adapter import list_documents, store_document, get_document


def store(args):
    logging.info(f"Running 'store'…")
    if args.list:
        logging.info(f"Getting list of files…")
        docs = list_documents()
        print("all docs on server:")
        for doc in docs:
            print(f"{doc[1]}, {doc[0]}")
        return
    # should store the doc to the database
    logging.info(f"Storing file…")
    with open(args.file) as file:
        # parses the text, currently we only support .txt files so we can just read it
        text = file.read()
        store_document(file, text, args.name, args.bank)
