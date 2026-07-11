from app.rag.components.text_splitter.chunks_validator import validate_chunks
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("EMBEDDER_API_URL")
EMBEDDER_KEY = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {EMBEDDER_KEY}"}

def embed_the_chunks(chunks: list,TIMEOUT: int) -> list:
    print(repr(API_URL))  # repr() will expose sneaky whitespace/\r/\n
    validated_batches = validate_chunks(chunks)
    total_embeddings = []
    for validated_chunks in validated_batches:
        payload = {"inputs": validated_chunks}
        response = requests.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
        if response.status_code != 200:
            raise Exception(
            f"Embedding the chunks failed | Status: {response.status_code} | Body: {response.text}"
            )
        embeddings = response.json()
        if not isinstance(embeddings, list):
            raise Exception("Invalid Response format")
        if not len(embeddings) == len(validated_chunks):
            raise Exception("Invalid Response size")
        total_embeddings.extend(embeddings)
    return total_embeddings


def embed_the_query(query_content:str, TIMEOUT=60) -> list:
    payload = {"inputs": query_content}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=TIMEOUT)
    if response.status_code != 200:
        raise Exception(
            f"Embedding the query failed | Status: {response.status_code} | Body: {response.text}"
        )
    embedded_query = response.json()
    return embedded_query
