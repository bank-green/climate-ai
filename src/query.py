from .openai_adapter import call_api
from .vectorize import search


def query(args):
    result_embedding_rows = search(args.bank, args.query)
    chunks = [r[2] for r in result_embedding_rows]
    response = call_api(args.query, chunks)

    formatted_chunks = "\n".join(chunks)

    print(
        f"""
The LLM was given the below excerpts from text about the bank to answer query."
CHUNKS
============
{formatted_chunks}

LLM RESPONSE
============
{response}

============

Do the above excerpts let you say YES to the question "{args.query}"?
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
