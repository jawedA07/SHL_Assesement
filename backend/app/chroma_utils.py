import chromadb
import os

PERSIST_DIR = os.getenv("CHROMA_DB_DIR", "db/chroma")


def get_client():
    """
    Returns a persistent Chroma client using the new API format.
    This ensures embeddings are stored locally and can be reloaded.
    """
    os.makedirs(PERSIST_DIR, exist_ok=True)  # Ensure directory exists
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    return client


def create_collection(name="shl_catalog"):
    """
    Creates a collection if it doesn't exist, otherwise retrieves it.
    """
    client = get_client()

    # Check if collection exists
    existing_collections = [c.name for c in client.list_collections()]
    if name in existing_collections:
        return client.get_collection(name)

    # Create new collection
    return client.create_collection(name=name)
