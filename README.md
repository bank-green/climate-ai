Currently working commands:
```
python cli.py store --bank the_co_operative_bank --name productpage --file docs/coop-products.html

python cli.py embed --bank the_co_operative_bank --name productpage  

python cli.py query --bank the_co_operative_bank --query "Does this bank offer free checking accounts?"

python cli.py query --bank triodos --query 'Does this bank give loans to coal-fired power plants?'
```






Goal: Database
-------------

## Texts
`id      human_name  parsed_text     file`

# Embeddings
`id      text_id     chunk_text      vector`   

# Queries
This Table does not exist yet.
`id      query       chunk_ids       llm_answer  human_answer`


Goal: Commands
--------------
These are not yet all implemented.

`store --name policy --bank triodos --file docs/policy.txt`

Stores the document and extracts the text.

`store --list --bank triodos`

Displays all stored documents for a bank.

`embed --name policy --bank the_co_operative_bank`

Chunkifies and vectorizes the document.

`embed --list --name policy --bank triodos`

Lists all chunks, displaying first 30 characters.

`embed --show --chunk-id`

Shows chunk.

`embed --flush --name policy --bank natwest`

Deletes all chunk and vectors for doc and bank.

`query --bank natwest --query 'Does this bank offer mobile banking?'`

Finds the most promising chunks and queries an LLM with based on them, outputs the judgment and requests a "yes/no/can't say" answer to whether the judgment is correct.
