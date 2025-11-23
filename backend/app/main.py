from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from .embeddings import embed_texts
from .chroma_utils import create_collection
from fastapi.middleware.cors import CORSMiddleware

COL_NAME = "shl_catalog"

app = FastAPI(title="SHL Assessment Recommender")

# Allow local frontend dev access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/recommend")
def recommend(req: RecommendRequest):
    q = req.query
    n = max(1, min(10, req.n_results or 5))

    if not q.strip():
        raise HTTPException(status_code=400, detail="query cannot be empty")

    q_emb = embed_texts([q])[0]
    col = create_collection(COL_NAME)
    results = col.query(query_embeddings=[q_emb], n_results=n, include=['metadatas','documents','distances'])
    out = []
    try:
        metadatas = results['metadatas'][0]
        docs = results['documents'][0]
        dists = results['distances'][0]
        for md, doc, dist in zip(metadatas, docs, dists):
            out.append({
                "assessment_name": md.get("name"),
                "assessment_url": md.get("url"),
                "description": md.get("description"),
                "meta": md.get("meta"),
                "score": float(dist)
            })
    except Exception:
        for hit in results:
            out.append(hit)
    return {"query": q, "n_results": len(out), "recommendations": out}
