import os
import openai


openai.organization = os.environ["OPENAI_ORGANISATION"]
openai.api_key = os.environ["OPENAI_API_KEY"]


def call_api(question, chunks):
    system_prompt = """You will be provided with exerpts from a bank's sustainability policy delimited by triple quotes and a question. Your task is to answer the question using only the provided excerpts and to cite the passage(s) of the document used to answer the question. If the excerpts do contain the information needed to answer this question then simply write: "Insufficient information." If an answer to the question is provided, it must be annotated with a citation. Use the following format for to cite relevant passages (reference: …)."""

    chunks_text = '"""' + '"""\n\n"""'.join(chunks) + '"""'

    user_prompt = chunks_text + "\n\n" + "Question: " + question

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
    res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    return res.choices[0].message.content
