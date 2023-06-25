import os, sys, dotenv

dotenv.load_dotenv()

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from src.database_adapter import store_questions
from src.embedders.e5BaseV2 import embed
import logging

print("Importing questions…")
with open("questions.txt") as questions_file:
    questions = questions_file.readlines()
    embeddings = embed([f"query: {question}" for question in questions])
    store_questions(questions=questions, embeddings=embeddings)
print("Done mporting questions.")
