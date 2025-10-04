#!/bin/bash
echo "🎨 Starting Streamlit frontend..."
source venv/bin/activate
streamlit run src/app.py --server.port 8501
