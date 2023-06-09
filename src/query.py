import logging
from .openai_adapter import call_api
from .embedders.e5BaseV2 import embed

from .database_adapter import (
    get_nearest_neighbors_and_question_from_question_id,
    store_questions,
)


def query_by_id(bank, question_id, chunks_only):
    chunk_rows, question_row = get_nearest_neighbors_and_question_from_question_id(
        bank, question_id
    )
    chunks = [row[2] for row in chunk_rows]
    question = question_row[0]
    if chunks_only:
        for chunk in chunks:
            print(f"{chunks}\n\n=================\n")
        return chunks
    else:
        ask_llm(question, chunks)


def store_question(question):
    question_embedding = embed([question])[0]
    new_question_id = store_questions([question], [question_embedding])
    logging.info(f"New id: {new_question_id[0]}")
    return new_question_id[0]


def ask_llm(question, chunks):
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
    return human_answer_typed, llm_assessment_typed
