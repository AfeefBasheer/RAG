from qdrant_client import QdrantClient

from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("QDRANT_ENDPOINT")
QDRANT_TIMEOUT = int(os.getenv("QDRANT_TIMEOUT", 60))
QDRANT_KEY = os.getenv("QDRANT_KEY")

qdrant_client = QdrantClient(
    url=API_URL, api_key=QDRANT_KEY, timeout=QDRANT_TIMEOUT, check_compatibility=False
)
