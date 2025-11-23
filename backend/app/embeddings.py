import os
import numpy as np

USE_OPENAI = os.getenv("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") is not None

if USE_OPENAI:
    import openai
    openai.api_key = os.getenv("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")

from sentence_transformers import SentenceTransformer

_local_model = None

def get_local_model():
    global _local_model
    if _local_model is None:
        _local_model = SentenceTransformer("all-MiniLM-L6-v2")
    return _local_model

def embed_texts(texts):
    if USE_OPENAI:
        resp = openai.Embedding.create(model="text-embedding-3-small", input=texts)
        embeddings = [e['embedding'] for e in resp['data']]
        return embeddings
    else:
        model = get_local_model()
        embs = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        return embs.tolist()
