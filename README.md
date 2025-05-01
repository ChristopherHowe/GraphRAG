# GraphRAG
## Data
## How Text Chunking is Performed
Chunking is very important
want to give the model as much relevant information as possible while avoiding distractors and fill the context window
Don't want to have chunks with contradicting information
Typical chunk sizes between 400-800 characters


# Knowledge Graph
## Neo4J
The actual neo4j database is ran inside of a docker container.
This docker container also contains neo4j browser which can be accessed via http://localhost:7474/browser/

## Entity Relationship Extraction
[Microsoft Entity Relationship Extraction Prompt](https://github.com/microsoft/graphrag/blob/main/graphrag/prompt_tune/prompt/entity_relationship.py#L6)


# Sources
[Medium GraphRAG Article](https://medium.com/@zilliz_learn/graphrag-explained-enhancing-rag-with-knowledge-graphs-3312065f99e1)
[Rebel Large Model](https://huggingface.co/Babelscape/rebel-large)
[Introduction to Datasets and loaders](https://www.youtube.com/watch?v=mDEoJhQEIuY)
[Linq Embedd Model](https://huggingface.co/Linq-AI-Research/Linq-Embed-Mistral), chosen because at top of [embedding leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
[Qdrant Guide on how to set up graphRAG](https://qdrant.tech/documentation/examples/graphrag-qdrant-neo4j)