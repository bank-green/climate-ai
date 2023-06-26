from flask import Flask, jsonify, request
from src.query import query_by_id, store_question
from src.database_adapter import get_questions_with_ids

import logging
import sys
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)

logging.info("Starting API server...")


app = Flask(__name__)


@app.route("/api/questions", methods=["GET"])
def api_list_questions():
    question_rows = get_questions_with_ids()
    questions = []
    for row in question_rows:
        question = {"id": row[0], "question": row[1]}
        questions.append(question)
    return jsonify(questions)


@app.route("/api/questions/<string:bank>/<int:question_id>", methods=["GET"])
def api_get_question(bank, question_id):
    chunks_only = bool(request.args.get("chunks_only"))
    question = query_by_id(bank, question_id, chunks_only)
    return jsonify(question)


@app.route("/api/questions", methods=["POST"])
def api_store_question():
    new_question = request.json["new_question"]
    question_in_db = store_question(new_question)
    return jsonify(question_in_db)


if __name__ == "__main__":
    app.run()