import logging
from .database_adapter import store_document, get_document_text_and_id, store_chunks
from readabilipy import simple_json_from_html_string
from .chunkify import chunkify
import fitz


def store(name, bank, filename):
    if filename.endswith(".txt"):
        logging.info(f"Reading .txt file {filename}…")
        file = open(filename)
        text = file.read()
        file.close()
    elif filename.endswith(".pdf"):
        logging.info(f"Parsing .pdf file {filename}…")
        doc = fitz.open(filename)
        text = ""
        for p in range(doc.page_count):
            text += doc.load_page(p).get_text()
        doc.close()
    elif filename.endswith(".html"):
        logging.info(f"Parsing .html file {filename}…")
        file = open(filename)
        html = file.read()
        text_as_list = simple_json_from_html_string(html)["plain_text"]
        text = "\n\n".join([e["text"] for e in text_as_list])
        file.close()
    else:
        raise ValueError("Document has unknown ending.")
    logging.info(f"Storing file…")
    with open(filename, "rb") as file:
        store_document(file, text, name, bank)


def chunkify_and_embed(name, bank):
    from .embedders.e5BaseV2 import embed

    logging.info("Running 'embed'…")
    logging.info("Retrieving document…")
    text, document_id = get_document_text_and_id(name, bank)

    logging.info("Chunkifying file…")
    chunks = chunkify(text)
    logging.info(f"Embedding {len(chunks)} chunks…")
    chunks_as_passages = ["passage: " + c for c in chunks]
    vectors = embed(chunks_as_passages)
    logging.info("Storing chunks with vectors…")
    store_chunks(chunks=chunks, embeddings=vectors, document_id=document_id)


def store_and_chunkify_and_embed(name, bank, file):
    logging.info(f"Running 'store'…")
    store(name, bank, file)
    chunkify_and_embed(name, bank)
