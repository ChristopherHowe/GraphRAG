from qdrant_client import QdrantClient, models
import os
import uuid

class MyQdrant:
    def __init__(self, collection_name: str, vec_size: int):
        port=os.getenv('QDRANT_PORT')
        self.client = QdrantClient(url=f"http://localhost:{port}")
        self.collection=collection_name
        self.vec_size=vec_size
        self._ensure_collection()

    def _ensure_collection(self):
        try:
            collection_info = self.client.get_collection(self.collection) # Throws an error if collection does not exist
            print(f"Skipping creating collection; '{self.collection}' already exists.")
        except Exception as e:
            if 'Not found: Collection' in str(e):
                print(f"Collection '{self.collection}' not found. Creating it now...")
                self.client.create_collection(
                    collection_name=self.collection,
                    vectors_config=models.VectorParams(size=self.vec_size, distance=models.Distance.COSINE)
                )

                print(f"Created Collection '{self.collection}'")
            else:
                print(f"Error while checking collection: {e}")
    
    def add_points(self,embedding_vals, content_ids):
        self.client.upsert(
        collection_name=self.collection,
        points=[
            {
                "id": str(uuid.uuid4()),
                "vector": embedding,
                "payload": {"id": content_id}
            }
            for content_id, embedding in zip(content_ids, embedding_vals)
        ]
    )