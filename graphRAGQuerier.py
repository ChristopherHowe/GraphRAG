from neo4j_funcs import Neo4j_Driver
from my_qdrant import MyQdrant
from EntityRelationshipExtractor import ER_Extractor
from utils import Sentence_Extractor
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from ollama import OllamaClient
from db_funcs import get_articles_by_ids, get_db_con
from utils import jupyter_print_paragraph
from langchain.prompts import PromptTemplate




class GraphRagQuerier:
    def __init__(self):
        load_dotenv()
        self.neo4j = Neo4j_Driver()
        self.qdrant = MyQdrant(
            os.getenv('QDRANT_COLLECTION_NAME'),os.getenv('QDRANT_VECTOR_SIZE'),
        )
        self.er_extractor = ER_Extractor()
        self.sentence_extractor=Sentence_Extractor()
        self.embedding_generator=SentenceTransformer("all-MiniLM-L6-v2")
        self.llmModel=OllamaClient()
    
    def query(self, prompt):
        related_embeddings = self._qdrant_inference(prompt)
        print(f"Related embeddings from Qdrant: {related_embeddings}")
        
        relationships, related_content = self._neo4j_inference(prompt)
        print(f"Relationships from Neo4j: {relationships}")
        print(f"Related content from Neo4j: {related_content}")
        
        top_qdrant = sorted(related_embeddings, key=lambda x: x[0], reverse=True)[:3]
        print(f"Top Qdrant results: {top_qdrant}")
        qdrant_content_ids = [payload['id'] for _, payload in top_qdrant]
        print(f"Qdrant content IDs: {qdrant_content_ids}")
        
        top_neo4j = sorted(related_content.items(), key=lambda x: x[1], reverse=True)[:3]
        print(f"Top Neo4j results: {top_neo4j}")
        neo4j_content_ids = [content_id for content_id, _ in top_neo4j]
        print(f"Neo4j content IDs: {neo4j_content_ids}")

        # Combine and deduplicate content IDs
        all_content_ids = list(set(qdrant_content_ids + neo4j_content_ids))
        print(f"All combined content IDs: {all_content_ids}")

        with get_db_con().cursor() as curr:
            content_blocks=[article[2] for article in get_articles_by_ids(curr, all_content_ids)]

        # Serialize the knowledge graph relationships
        relationships_str = "\n".join([str(rel) for rel in relationships])

        # Prepare context for LangChain
        context = (
            "Relevant Articles:\n"
            + "\n---\n".join(content_blocks)
            + "\n\nKnowledge Graph Relationships:\n"
            + relationships_str
        )

        # Create a prompt template
        prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="Given the following context:\n{context}\n\nAnswer the question:\n{question}"
        )

        full_prompt = prompt_template.format(context=context, question=prompt)
        response=self.llmModel.generate(full_prompt)
        return full_prompt,response

    def _qdrant_inference(self, prompt):
        embedding=self.embedding_generator.encode(prompt)
        print(embedding)
        vectors=self.qdrant.retrieve(embedding)
        return [(vector.score, vector.payload) for vector in vectors]
         
    
    def _neo4j_inference(self, prompt):
        sentences = self.sentence_extractor.get_sentences(prompt)        
        er_triplets = self.er_extractor.extract_ERs(sentences)

        entity_names = []
        for triplet in er_triplets:
            entity_names.append(triplet.head)
            entity_names.append(triplet.tail)
        print(f"Extracted entities from query: {entity_names}")

        nodes, relationships =  self.neo4j.get_subgraphs(entity_names)
        related_content = {} # Map storing content ids to their frequency in the related subgraph
        for node in nodes:
            for content_id in node.content_ids:
                if content_id in related_content:
                    related_content[content_id]+=1
                else:
                    related_content[content_id]=1
        
        return relationships, related_content
