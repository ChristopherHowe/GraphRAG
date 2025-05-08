import os
import requests
from dotenv import load_dotenv
import time

class OllamaClient:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("OLLAMA_HOST")
        self.port = os.getenv("OLLAMA_PORT")
        self.base_url = f"http://{self.host}:{self.port}"

    def generate(self, prompt, model="llama2", retries=3, backoff_factor=0.5):
        """Generate a response from the model with retry logic and streaming support."""

        payload = {"model": model, "prompt": prompt, "stream": False}
        for attempt in range(retries):
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except requests.RequestException as e:
                print(f"Retrying attempt: {attempt}")
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                else:
                    return {"error": str(e)}