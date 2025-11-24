# ---------- Base Image ----------
FROM python:3.10-slim

# ---------- Environment Vars ----------
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000

# ---------- Work Directory ----------
WORKDIR /app

# ---------- Install system deps (required by chromadb) ----------
RUN apt-get update && apt-get install -y \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- Copy backend files ----------
COPY backend/app /app

# ---------- Install python dependencies ----------
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- Expose Port ----------
EXPOSE 8000

# ---------- Start FastAPI ----------
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
