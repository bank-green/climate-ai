Currently working commands:
```
python cli.py store --bank the_co_operative_bank --name productpage --file docs/coop-products.html

python cli.py store --bank the_co_operative_bank --name productpage --no-embedding
python cli.py store --bank the_co_operative_bank --name productpage --embedding-only

python cli.py query --bank the_co_operative_bank --query "Does this bank offer free checking accounts?"

python cli.py query --bank triodos --query 'Does this bank give loans to coal-fired power plants?'
```

Technical Design: https://app.nuclino.com/BankGreen/ClimateAI/Technical-Design-381f6db0-c54d-4b1d-9f24-f0f468b5a19d