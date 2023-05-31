import os
import openai
from pathlib import Path
from dotenv import load_dotenv


openai.organization = os.environ["OPENAI_ORGANISATION"]
openai.api_key = os.environ["OPENAI_API_KEY"]


def call_api(query, chunks):
    system_prompt = "You are a helpful assistant. Your answers are concise. You answer in no more than 4 sentences, excluding references. You do not use paragraph breaks. Your answer ends with a clear 'YES' or 'NO'."
    user_prompt = "I am providing you with various excerpts of text describing the feature offerings or sustainability policies of a bank. I will ask you about what financing it allows or forbids. If financing for a company or project is not explicitly prohibited, then consider it allowed."

    input_text = "\n\n".join(chunks)

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt,
        },
        {
            "role": "user",
            "content": input_text,
        },
        {"role": "user", "content": query},
        {
            "role": "user",
            "content": "Provide references to the parts of the text you were given that justify your answer. If possible, provide explicit citations. Make sure the sections cited exist in the given texts.",
        },
    ]
    res = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    return res.choices[0].message.content
