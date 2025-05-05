import os
import requests
from dotenv import load_dotenv
import time
import json

class OllamaClient:
    def __init__(self):
        load_dotenv()
        self.host = os.getenv("OLLAMA_HOST")
        self.port = os.getenv("OLLAMA_PORT")
        self.base_url = f"http://{self.host}:{self.port}"

    # def health(self):
    #     """Check if the Ollama server is running."""
    #     try:
    #         response = requests.get(f"{self.base_url}/health")
    #         response.raise_for_status()
    #         return response.json()
    #     except requests.RequestException as e:
    #         return {"error": str(e)}

    # def list_models(self):
    #     """List available models."""
    #     try:
    #         response = requests.get(f"{self.base_url}/api/tags")
    #         response.raise_for_status()
    #         return response.json()
    #     except requests.RequestException as e:
    #         return {"error": str(e)}

    def generate(self, prompt, model="llama2", retries=3, backoff_factor=0.5):
        """Generate a response from the model with retry logic and streaming support."""

        payload = {"model": model, "prompt": prompt, "stream": False}
        for attempt in range(retries):
            try:
                response = requests.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    stream=False  # This can also be omitted, as it's not needed for non-streamed
                )
                response.raise_for_status()
                data = response.json()
                return data.get("response", "")
            except requests.RequestException as e:
                print(f"Retrying attempt: {attempt}")
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))  # Exponential backoff
                else:
                    return {"error": str(e)}

# Example usage:
# client = OllamaClient()
# print(client.health())
# print(client.list_models())
# print(client.generate("Hello, world!"))