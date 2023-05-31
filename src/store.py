from .database_adapter import store_document, get_document


def store(args):
    # should store the doc to the database
    with open(args.file) as file:
        # parses the text, currently we only support .txt files so we can just read it
        text = file.read()
        store_document(file, text, args.name, args.bank)
