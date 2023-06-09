from flask import Flask, jsonify, request
from flask_cors import CORS
from src.query import query_by_id, store_question
from src.database_adapter import get_questions_with_ids, list_documents, list_banks
from src.query import query_by_id
from src.store import save_from_url, store_and_chunkify_and_embed

import sys

import logging

logging.basicConfig(
    level=logging.DEBUG,
    stream=sys.stdout,
    format="%(asctime)s %(message)s",
    datefmt="%H:%M:%S",
)
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
CORS(app)


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
    new_question = request.json["newQuestion"]
    question_in_db = store_question(new_question)
    return jsonify(question_in_db)


@app.route("/api/documents/<string:bank>", methods=["GET"])
def api_list_documents(bank):
    document_rows = list_documents(bank)
    documents = [r[0] for r in document_rows]
    return jsonify(documents)


@app.route("/api/query", methods=["POST"])
def api_ask_question():
    question_id = request.json["questionId"]
    bank = request.json["bank"]
    response_dict = query_by_id(bank, question_id)
    return jsonify({"response": response_dict["llm_response"], "chunks": response_dict["chunks"]})

@app.route("/api/documents", methods=["POST"])
def api_store_link():
    url = request.json["url"]
    bank = request.json["bank"]
    name = request.json["name"]
    file = save_from_url(url)
    store_and_chunkify_and_embed(name, bank, file)
    return "ok"

@app.route("/api/banks", methods=["GET"])
def api_list_banks():
    bank_rows = list_banks()
    banks = [{"tag": row[0], "name": row[1]} for row in bank_rows]
    return jsonify(banks)


if __name__ == "__main__":
    app.run()
