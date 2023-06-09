# Setup
The setup expects `virtualenv`, `make`, and `npm` to be installed.
```
make init
make run
```

When you run your first command, things might take a while longr as HuggingFace has to download our embedding model that is not installed as part of the module.

# Basic Backend Commands

Currently working commands:
```
python cli.py store --bank natwest --name policy --file docs/natwest.txt
python cli.py store --bank natwest --name policy --file docs/natwest.txt --no-embeddings
python cli.py store --bank natwest --name policy --file docs/natwest.txt --embeddings-only

python cli.py query --list-questions
python cli.py query --bank natwest --new-question 'Does this bank give loans to coal-fired power plants?'
python cli.py query --bank natwest --question-id 2 --chunks-only
```
# Technical Design
https://app.nuclino.com/BankGreen/ClimateAI/Technical-Design-381f6db0-c54d-4b1d-9f24-f0f468b5a19d