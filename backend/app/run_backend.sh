#!/bin/bash
# Activate venv and run backend (example)
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
