import requests
import os

API_URL = os.getenv("RERANKER_API_URL")
RERANKER_KEY = os.getenv("HF_TOKEN")

headers = {"Authorization": f"Bearer {RERANKER_KEY}"}
def rerank_the_vector(query: str, chunks: list[str], timeout: int = 30):

    payload = {
        "inputs": [
            {
                "text": query,
                "text_pair": chunk
            }
            for chunk in chunks
        ]
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=timeout
    )

    response.raise_for_status()

    scores = response.json()[0]

    reranked = []

    for index, item in enumerate(scores):

        reranked.append({
            "index": index,
            "score": item["score"]
        })

    reranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return reranked