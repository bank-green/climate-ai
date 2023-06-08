import logging
from .openai_adapter import call_api
from .embedders.e5BaseV2 import (
    search as search_e5BaseV2,
)

from .database_adapter import get_embedding_rows


def search(bank, query):
    logging.info("Retrieving all embeddings…")
    embedding_rows = get_embedding_rows(bank)
    # logging.info(f"Searching for nearest neighbors in {len(embedding_rows)} embeddings.")
    results = search_e5BaseV2(embedding_rows, query)
    chunks = [r[2] for r in results]
    return chunks


def query_by_id(bank, query_id):
    raise NotImplementedError()


def store_query(bank, query):
    raise NotImplementedError()


def query_by_new_query(bank, query):
    # should first run store_query, then query_by_id

    logging.info("Running 'query'…")
    logging.info(f"Getting nearest neighbors.")
    chunks = search(bank, query)

    logging.info(f"Calling API with {len(chunks)} nearest-neighbor chunks…")
    response = call_api(query, chunks)
    logging.info(f"Got response.")

    formatted_chunks = "\n------------------------------------------------------------------------\n".join(
        chunks
    )

    print(
        f"""
The LLM was given the below excerpts from text about the bank to answer query "{query}"
CHUNKS
============
{formatted_chunks}

LLM RESPONSE
============
{response}

============

What is the answer to the question "{query}"?
"""
    )
    human_answer = input("(Y)es/(N)o: ")
    human_answer_typed = True if human_answer == "Y" else False

    print(
        f"""
Did the LLM correctly and clearly answer the question?
        """
    )
    llm_assessment = input("(Y)es/(N)o: ")
    llm_assessment_typed = True if llm_assessment == "Y" else False

    print(f"Human answer to query: {human_answer_typed}")
    print(f"Did LLM get it right: {llm_assessment_typed}")
