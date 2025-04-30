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

    def insert_relationship(self, subject, subject_type, predicate, object, object_type):
        """
        Insert a relationship triplet into Neo4j.
        Creates nodes if they don't exist and connects them with the predicate relationship.
        """
        with self.driver.session() as session:
            query = """
                MERGE (s:`{subject_type}` {{name: $subject}})
                MERGE (o:`{object_type}` {{name: $object}})
                MERGE (s)-[r:`{predicate}`]->(o)
                RETURN s, r, o
            """.format(subject_type=subject_type, object_type=object_type, predicate=predicate)


            try:
                result = session.run(query, subject=subject, object=object)
                return result.single()
            except Exception as e:
                print(f"Error inserting relationship: {e}")
                return None

    def close_connection(self):
            self.driver.close()