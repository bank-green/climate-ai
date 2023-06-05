import logging
from .openai_adapter import call_api
from .vectorize import search


def query(args):
    logging.info("Running 'query'…")
    logging.info(f"Getting nearest neighbors.")
    result_embedding_rows = search(args.bank, args.query)

    chunks = [r[2] for r in result_embedding_rows]

    logging.info(f"Calling API with {len(chunks)} nearest-neighbor chunks…")
    response = call_api(args.query, chunks)
    logging.info(f"Got response.")

    formatted_chunks = "\n------------------------------------------------------------------------\n".join(
        chunks
    )

    print(
        f"""
The LLM was given the below excerpts from text about the bank to answer query "{args.query}"
CHUNKS
============
{formatted_chunks}

LLM RESPONSE
============
{response}

============

What is the answer to the question "{args.query}"?
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
