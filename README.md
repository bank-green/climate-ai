# Setup
```
source venv/bin/activate
pip install -r requirements.txt
```

When you run your first command, things might take a while longr as HuggingFace has to download our embedding model that is not installed as part of the module.

# Basic Commands

Currently working commands:
```
python cli.py store --bank natwest --name policy --file docs/natwest.txt
python cli.py store --bank natwest --name policy --file docs/natwest.txt --no-embeddings
python cli.py store --bank natwest --name policy --file docs/natwest.txt --embeddings-only

python cli.py query --bank natwest --question 'Does this bank give loans to coal-fired power plants?'
python cli.py query --bank natwest --question 'Does this bank give loans to coal-fired power plants?' --chunks-only
```
# Technical Design
https://app.nuclino.com/BankGreen/ClimateAI/Technical-Design-381f6db0-c54d-4b1d-9f24-f0f468b5a19d