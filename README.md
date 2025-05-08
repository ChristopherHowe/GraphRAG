# HybridRAG Exploration

## Overview
This project is an exploration into hybridRAG architectures. The system enhances the quality of responses from large language models (LLMs) by combining vector-based and knowledge graph-based retrieval methods. This approach minimizes hallucinations and improves the factual accuracy of model outputs.

## Project Architecture
It's is built with a modular, service-oriented architecture using Docker containers:
- **Relational Database (Postgres)**: Stores raw text data and metadata.
- **Vector Database (Qdrant)**: Stores vector embeddings of text chunks for semantic search.
- **Knowledge Graph (Neo4j)**: Stores entities and their relationships extracted from text data.
- **Language Model (Ollama 2)**: Generates responses using a combination of vector and graph data.

## Installation
### Prerequisites
- Docker and Docker Compose
- Conda (for Python environment management)
- Python 3.8+

### Setup Steps
1. Start Docker Containers:
```bash
docker compose up -d
```

2. Set Up Python Environment:
```bash
conda create -n GraphRAG
conda activate GraphRAG
pip install -r requirements.txt
```

3. Apply Database Migrations:
```bash
python3 migrate.py
```

### Restarting Containers
To restart the system and reset data:
```bash
docker compose down
docker volume prune --all
docker compose up -d
```

### Example `.env` file
```bash
# PostgreSQL Configuration
DB_USER=postgresUser
DB_PASSWORD=postgresPass
DB_NAME=GraphRag
DB_PORT=5432

# Neo4j Configuration
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4jPass
NEO4J_HTTP_PORT=7474
NEO4J_BOLT_PORT=7687

# QDrant Configuration
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=graphRAG
QDRANT_VECTOR_SIZE=384

# Ollama Configuration
OLLAMA_PORT=11434
OLLAMA_HOST=localhost
```

## Data Ingestion
Data ingestion is managed through the `ingestion.ipynb` notebook and involves three main steps:
1. **Relational Database Ingestion**: Raw text data is loaded into the PostgreSQL database, including articles, questions, and metadata.
2. **Vector Embedding Generation**: Each text block is converted into a vector using a pre-trained model, and these vectors are stored in Qdrant.
3. **Knowledge Graph Creation**: Entities and relationships are extracted from text using the Rebel model, and these are stored in Neo4j.

## Query Execution
Querying is managed through the `query.ipynb` notebook and follows a multi-step process:
1. **User Query Vectorization**: The query is vectorized using the same model as for ingestion.
2. **Vector Search**: The query vector is used to find the most relevant text blocks in Qdrant.
3. **Entity Extraction and Graph Search**: Entities are extracted from the query, and related entities are retrieved from Neo4j.
4. **Response Generation**: The retrieved text blocks and entity relationships are passed to the Ollama2 model, which generates the final response.

## Future Improvements
- Enhanced entity relationship extraction using an ontology.
- Improved query selection logic.
- Advanced graph structure with richer relationships.

## Sources
### Research Papers
- [Microsoft GraphRAG Original Paper (2023)](https://arxiv.org/abs/2404.16130)
- [HybridRAG Paper (2024)](https://arxiv.org/abs/2408.04948)
- [Original RAG Paper (2020)](https://arxiv.org/abs/2005.11401)

### Model References
- [Rebel Large Model](https://huggingface.co/Babelscape/rebel-large)
- [Linq Embedd Model](https://huggingface.co/Linq-AI-Research/Linq-Embed-Mistral)
- [Phi 2 LLM Model](https://huggingface.co/microsoft/phi-2)
- [Ollama2 Model](https://www.llama.com/llama2/)

### Tutorials and Guides
- [Qdrant GraphRAG Setup Guide](https://qdrant.tech/documentation/examples/graphrag-qdrant-neo4j)
- [Microsoft Entity Relationship Extraction Prompt](https://github.com/microsoft/graphrag/blob/main/graphrag/prompt_tune/prompt/entity_relationship.py#L6)
