from neo4j import GraphDatabase
import os
from models import triplet
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel


class GraphRAGNode(BaseModel):
    name: str
    content_ids: List[int]
    

class Neo4j_Driver:
    def __init__(self):
        load_dotenv()
        uri = f"bolt://localhost:{os.getenv('NEO4J_BOLT_PORT')}"
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASSWORD')
        self.driver=GraphDatabase.driver(uri, auth=(user, password))

    def insert_relationship(self, subject, subject_type, predicate, object, object_type, content_id):
        """
        Insert a relationship triplet into Neo4j.
        Creates nodes if they don't exist and connects them with the predicate relationship.
        Updates the content_id array on both subject and object nodes.
        """
        with self.driver.session() as session:
            query = """
                MERGE (s:`{subject_type}` {{name: $subject}})
                ON CREATE SET s.content_ids = [$content_id]
                ON MATCH SET s.content_ids = CASE WHEN NOT $content_id IN s.content_ids THEN s.content_ids + $content_id ELSE s.content_ids END
                MERGE (o:`{object_type}` {{name: $object}})
                ON CREATE SET o.content_ids = [$content_id]
                ON MATCH SET o.content_ids = CASE WHEN NOT $content_id IN o.content_ids THEN o.content_ids + $content_id ELSE o.content_ids END
                MERGE (s)-[r:`{predicate}`]->(o)
                RETURN s, r, o
            """.format(subject_type=subject_type, object_type=object_type, predicate=predicate)

            try:
                result = session.run(query, subject=subject, object=object, content_id=content_id)
                return result.single()
            except Exception as e:
                print(f"Error inserting relationship: {e}")
                return None

    def get_subgraphs(self, entity_names):
        """
        Gets all subgraphs of the overall database formed by all nodes 1-2 hops away from every node in entity_names.
        
        Args:
            entity_names (list): List of entity names to search for
            
        Returns:
            tuple: (nodes, relationships) where nodes is a list of GraphRAGNode objects and 
            relationships is a list of tuples (source_name, relationship_type, target_name)
        """
        query = """
            MATCH (e:entity)-[r1]-(n1)-[r2]-(n2)
            WHERE toLower(e.name) IN [name IN $entity_names | toLower(name)]
            RETURN e, r1 as r, n1, r2, n2
            UNION
            MATCH (e:entity)-[r]-(n1)
            WHERE toLower(e.name) IN [name IN $entity_names | toLower(name)]
            RETURN e, r, n1, null as r2, null as n2
        """
        
        with self.driver.session() as session:
            result = session.run(query, entity_names=entity_names)
            
            # Use set for efficient duplicate checking
            node_names = set()
            nodes: List[GraphRAGNode] = []
            relationships = []

            def add_node(neo4j_node) -> List[GraphRAGNode]:
                """Helper function to add a node if it doesn't exist"""
                name = neo4j_node["name"]
                if name not in node_names:
                    nodes.append(GraphRAGNode(
                        name=name,
                        content_ids=neo4j_node.get("content_ids", [])
                    ))
                    node_names.add(name)

            for record in result:
                # Add nodes
                add_node(record["e"])
                add_node(record["n1"])
                if record["n2"]:
                    add_node(record["n2"])
                
                # Add relationships
                relationships.append((
                    record["e"]["name"],
                    record["r"].type,
                    record["n1"]["name"]
                ))
                
                if record["n2"]:
                    relationships.append((
                        record["n1"]["name"],
                        record["r2"].type,
                        record["n2"]["name"]
                    ))

            return nodes, relationships

    def close_connection(self):
            self.driver.close()