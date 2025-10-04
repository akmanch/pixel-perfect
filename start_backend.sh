#!/bin/bash
echo "🚀 Starting FastAPI backend..."
source venv/bin/activate
uvicorn src.main:app --reload --port 8000 --host 0.0.0.0
