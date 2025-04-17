from neo4j import GraphDatabase
import os
from dotenv import load_dotenv


class Neo4j_Driver:
    def __init__(self):
        load_dotenv()
        uri = f"bolt://localhost:{os.getenv('NEO4J_BOLT_PORT')}"
        user = os.getenv('NEO4J_USER')
        password = os.getenv('NEO4J_PASSWORD')
        self.driver=GraphDatabase.driver(uri, auth=(user, password))

    def insert_relationship(self, subject, predicate, object):
        """
        Insert a relationship triplet into Neo4j.
        Creates nodes if they don't exist and connects them with the predicate relationship.
        """
        with self.driver.session() as session:
            query = """
            MERGE (s:Entity {name: $subject})
            MERGE (o:Entity {name: $object})
            MERGE (s)-[r:RELATIONSHIP {type: $predicate}]->(o)
            RETURN s, r, o
            """
            try:
                result = session.run(query, subject=subject, predicate=predicate, object=object)
                return result.single()
            except Exception as e:
                print(f"Error inserting relationship: {e}")
                return None

    def close_connection(self):
            self.driver.close()