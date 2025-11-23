import pandas as pd
from .embeddings import embed_texts
from .chroma_utils import create_collection
import os

CSV_PATH = os.getenv("SHL_CSV", "data/shl_catalog.csv")
COL_NAME = "shl_catalog"


def index_csv():
    df = pd.read_csv(CSV_PATH)

    # combine fields for embedding
    df["text_to_embed"] = (
        df["name"].fillna("")
        + " . "
        + df["description"].fillna("")
        + " . "
        + df["meta"].fillna("")
    )

    texts = df["text_to_embed"].tolist()
    print(f"Computing embeddings for {len(texts)}...")

    # generate embeddings
    embeddings = embed_texts(texts)
    ids = [str(i) for i in range(len(texts))]

    # connect to Chroma collection
    col = create_collection(COL_NAME)

    # metadata to store along with the embeddings
    metadatas = (
        df[["name", "url", "description", "meta"]].fillna("").to_dict(orient="records")
    )

    # NEW API: use UPSERT instead of ADD
    col.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts)

    print(f"✔ Successfully indexed {len(ids)} items into Chroma!")


if __name__ == "__main__":
    index_csv()
