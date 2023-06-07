import logging
from .database_adapter import store_document, get_document, store_chunks
from .embedders.e5BaseV2 import (
    vectorize as vectorize_e5BaseV2,
)


def store(name, bank, file):
    text = file.read()
    logging.info(f"Storing file…")
    store_document(file, text, name, bank)


def chunkify(text):
    # simply cuts up the text into equal pieces

    # separator = "\n\n"
    # min_chunk_length = 40
    # chunks = text.split(separator)
    # long_chunks = [chunk for chunk in chunks if len(chunk) > min_chunk_length]
    chunk_size = 1000
    long_chunks = [
        text[start : start + chunk_size] for start in range(0, len(text), chunk_size)
    ]
    return long_chunks


def embed(name, bank):
    logging.info("Running 'embed'…")
    logging.info("Retrieving document…")
    text, document_id = get_document(name, bank)

    logging.info("Chunkifying file…")
    chunks = chunkify(text)
    logging.info(f"Embedding {len(chunks)} chunks…")
    vectors = vectorize_e5BaseV2(chunks=chunks)
    logging.info("Storing chunks with vectors…")
    store_chunks(chunks=chunks, vectors=vectors, document_id=document_id)


def store_and_embed(name, bank, file):
    logging.info(f"Running 'store'…")
    # should store the doc to the database
    store(name, bank, file)
    embed(name, bank)
