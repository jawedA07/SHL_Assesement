FROM python:3.10

WORKDIR /app

# Copy requirements from correct path
COPY backend/app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the full backend project folder
COPY backend /app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
