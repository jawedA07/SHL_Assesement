FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y \
    curl build-essential gcc libsqlite3-dev && \
    apt clean

# Speed up pip
RUN pip install --upgrade pip setuptools wheel

COPY backend/app/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
