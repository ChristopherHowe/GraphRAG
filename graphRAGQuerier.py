from neo4j_funcs import Neo4j_Driver
from my_qdrant import MyQdrant
from EntityRelationshipExtractor import ER_Extractor
from utils import Sentence_Extractor
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer





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
        self.llmModel = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", torch_dtype="auto", trust_remote_code=True)
        self.llmTokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)

    
    def query(self, prompt):
        related_embeddings=self._qdrant_inference(prompt)
        relationships, related_content= self._neo4j_inference(prompt)
        inputs = self.llmTokenizer('''def print_prime(n):
        """
        Print all primes between 1 and n
        """''', return_tensors="pt", return_attention_mask=False)

        outputs = self.llmModel.generate(**inputs, max_length=200)
        text = self.llmTokenizer.batch_decode(outputs)[0]
        print(text)


    def _qdrant_inference(self, prompt):
        embedding=self.embedding_generator.encode(prompt)
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
