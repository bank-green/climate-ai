from .embedders.e5BaseV2 import (
    vectorize as vectorize_e5BaseV2,
    search as search_e5BaseV2,
)

from .database_adapter import get_embedding_rows, get_document, store_chunks


def embed(args):
    text, document_id = get_document(args.name, args.bank)

    chunks = chunkify(text)
    vectors = vectorize_e5BaseV2(chunks=chunks)
    store_chunks(chunks=chunks, vectors=vectors, document_id=document_id)


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


def search(bank, query):
    embedding_rows = get_embedding_rows(bank)
    results = search_e5BaseV2(embedding_rows, query)
    return results
