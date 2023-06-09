import logging
from .openai_adapter import call_api
from .embedders.e5BaseV2 import embed

from .database_adapter import (
    get_embedding_rows,
    get_nearest_neighbor_from_embedding,
    store_questions,
)


def search(bank, question):
    logging.info("Retrieving all embeddings…")

    question_embedding = embed([question])[0]
    results = get_nearest_neighbor_from_embedding(bank, question_embedding)
    chunks = [row[2] for row in results]
    return chunks


def query_by_id(bank, question_id):
    raise NotImplementedError()


def store_question(question):
    question_embedding = embed([question])[0]
    new_question_id = store_questions([question], [question_embedding])
    print(f"New id: {new_question_id[0]}")
    return new_question_id[0]


def query_by_new_question(bank, question):
    # should first run store_query, then query_by_id

    logging.info("Running 'query'…")
    logging.info(f"Getting nearest neighbors.")
    chunks = search(bank, question)

    logging.info(f"Calling API with {len(chunks)} nearest-neighbor chunks…")
    response = call_api(question, chunks)
    logging.info(f"Got response.")

    formatted_chunks = "\n------------------------------------------------------------------------\n".join(
        chunks
    )

    print(
        f"""
The LLM was given the below excerpts from text about the bank to answer query "{question}"
CHUNKS
============
{formatted_chunks}

LLM RESPONSE
============
{response}

============

What is the answer to the question "{question}"?
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
