import logging
from .openai_adapter import call_api
from .embedders.e5BaseV2 import embed

from .database_adapter import (
    get_nearest_neighbors_and_question_from_question_id,
    store_questions,
)


def query_by_id(bank, question_id, chunks_only=False):
    chunk_rows, question_row = get_nearest_neighbors_and_question_from_question_id(
        bank, question_id
    )
    chunks = [row[2] for row in chunk_rows]
    question = question_row[0]
    if chunks_only:
        return {"r_type": "chunks", "chunks": chunks, "question": question}
    else:
        llm_response = ask_llm(question, chunks)
        return {
            "r_type": "llm",
            "chunks": chunks,
            "llm_response": llm_response,
            "question": question,
        }


def store_question(question):
    question_embedding = embed([question])[0]
    new_question_id = store_questions([question], [question_embedding])
    logging.info(f"New id: {new_question_id[0]}")
    return new_question_id[0]


def ask_llm(question, chunks):
    logging.info(f"Calling API with {len(chunks)} nearest-neighbor chunks…")
    response = call_api(question, chunks)
    logging.info(f"Got response.")
    return response
