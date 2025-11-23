import pandas as pd
import numpy as np
from .embeddings import embed_texts
from .chroma_utils import create_collection
import os
import csv

EXCEL_PATH = os.getenv("GEN_AI_EXCEL", "/mnt/data/Gen_AI Dataset.xlsx")
COL_NAME = "shl_catalog"

def load_train_labels():
    x = pd.ExcelFile(EXCEL_PATH)
    for s in x.sheet_names:
        df = x.parse(s)
        if 'Query' in df.columns or 'query' in df.columns:
            return df
    return x.parse(x.sheet_names[0])

def mean_recall_at_k(k=10):
    df = load_train_labels()
    if 'Query' in df.columns:
        queries = df['Query'].astype(str).tolist()
    elif 'query' in df.columns:
        queries = df['query'].astype(str).tolist()
    else:
        queries = df.iloc[:,0].astype(str).tolist()

    if 'Relevant' in df.columns:
        gt = df['Relevant'].tolist()
    elif 'Label' in df.columns:
        gt = df['Label'].tolist()
    else:
        gt = df.iloc[:,1].astype(str).tolist()

    col = create_collection(COL_NAME)
    recalls = []
    for q, g in zip(queries, gt):
        q_emb = embed_texts([q])[0]
        res = col.query(query_embeddings=[q_emb], n_results=k, include=['metadatas'])
        metas = res['metadatas'][0]
        retrieved_urls = [m.get('url') for m in metas if m.get('url')]
        true = [x.strip() for x in str(g).split(",") if x.strip()]
        if len(true) == 0:
            continue
        found = sum(1 for u in retrieved_urls if any(t in u for t in true) or u in true)
        recall = found / len(true)
        recalls.append(recall)
    mean_recall = float(np.mean(recalls)) if recalls else 0.0
    print(f"MeanRecall@{k}: {mean_recall:.4f}")
    return mean_recall

def create_submission_csv(output_path="submission.csv", k=10):
    xls = pd.ExcelFile(EXCEL_PATH)
    sheets = xls.sheet_names
    df_test = None
    for s in sheets:
        if 'test' in s.lower() or 'unlabeled' in s.lower():
            df_test = pd.read_excel(EXCEL_PATH, sheet_name=s)
            break
    if df_test is None:
        if len(sheets) > 1:
            df_test = pd.read_excel(EXCEL_PATH, sheet_name=sheets[1])
        else:
            df_test = pd.read_excel(EXCEL_PATH, sheet_name=sheets[0])

    queries = df_test.iloc[:,0].astype(str).tolist()
    col = create_collection(COL_NAME)
    rows = []
    for q in queries:
        q_emb = embed_texts([q])[0]
        res = col.query(query_embeddings=[q_emb], n_results=k, include=['metadatas'])
        metas = res['metadatas'][0]
        urls = [m.get('url') for m in metas if m.get('url')]
        for u in urls:
            rows.append({"Query": q, "Assessment_url": u})
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Query","Assessment_url"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print("Saved submission CSV to", output_path)

if __name__ == "__main__":
    mean_recall_at_k(10)
    create_submission_csv("submission.csv", k=10)
