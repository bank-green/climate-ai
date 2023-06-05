import psycopg2
import os
from psycopg2 import extras
import logging

logging.info(f"Starting DB connection…")
conn = psycopg2.connect(
    host=os.environ["POSTGRES_HOST"],
    dbname=os.environ["POSTGRES_DBNAME"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
logging.info(f"Connected to DB.")

conn.set_session(autocommit=True)


def store_document(file, text, name, bank):
    cur = conn.cursor()

    # not storing the binary file yet
    cur.execute(
        'INSERT INTO documents ("bank", "file", "name", "text") VALUES (%s, %s, %s, %s)',
        (bank, None, name, text),
    )


def get_document(name, bank):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM documents WHERE name = %s AND bank = %s",
        (name, bank),
    )
    x = cur.fetchone()
    return x[3], x[0]


def store_chunks(chunks, vectors, document_id):
    assert len(chunks) == len(vectors)
    cur = conn.cursor()

    values = [[chunks[i], vectors[i], document_id] for i in range(0, len(chunks))]
    extras.execute_values(
        cur,
        'INSERT INTO embeddings ("chunk", "embedding", "document_id") VALUES %s',
        values,
    )


def get_embedding_rows(bank):
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM embeddings e INNER JOIN documents d ON e.document_id = d.id WHERE d.bank = %s",
        (bank,),
    )
    embedding_rows = cur.fetchall()
    return embedding_rows


def list_documents():
    cur = conn.cursor()

    cur.execute("SELECT name, bank FROM documents")
    documents = cur.fetchall()
    return documents
