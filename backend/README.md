# SHL Recommender Backend

Run:
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt

# Crawl SHL
python app/scrape_shl.py

# Index into Chroma
python app/index_embeddings.py

# Run server
uvicorn app.main:app --reload
