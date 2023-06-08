import psycopg2
from psycopg2 import extras
import os
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

import dotenv

dotenv.load_dotenv()

endpoint = "https://data.bank.green/graphql"

print("This might not catch all banktags since we are not paging through.")


def write_rows(values):
    print(f"Starting DB connection…")
    conn = psycopg2.connect(
        host=os.environ["POSTGRES_HOST"],
        dbname=os.environ["POSTGRES_DBNAME"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    print(f"Connected to DB.")
    conn.set_session(autocommit=True)

    cur = conn.cursor()
    print(f"Writing {len(values)} rows to DB.")
    extras.execute_values(
        cur,
        'INSERT INTO banks ("tag", "name") VALUES %s',
        values,
    )
    print(f"Done writing.")


def retrieve_banktags():
    transport = AIOHTTPTransport(url=endpoint)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    query = gql(
        """
        {
            brands {
                edges {
                node {
                    tag
                    name
                }
                }
            }
        }
    """
    )
    results = client.execute(query)
    values = [
        [elem["node"]["tag"], elem["node"]["name"]]
        for elem in results["brands"]["edges"]
    ]
    return values


values = retrieve_banktags()
write_rows(values)
print("Done.")
