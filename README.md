# GraphRAG
## Data
## How Text Chunking is Performed
Chunking is very important
want to give the model as much relevant information as possible while avoiding distractors and fill the context window
Don't want to have chunks with contradicting information
Typical chunk sizes between 400-800 characters



# Configuration
```
DB_NAME=squaddb
DB_USER=squaduser
DB_PASSWORD=squadpass
DB_HOST=localhost
DB_PORT=5432
```

# Neo4J
The actual neo4j database is ran inside of a docker container.
This docker container also contains neo4j browser which can be accessed via http://localhost:7474/browser/

# Sources
[Medium GraphRAG Article](https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1)
[Rebel Large Model](https://huggingface.co/Babelscape/rebel-large)
