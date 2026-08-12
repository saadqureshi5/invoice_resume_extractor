#!/bin/bash
# start.sh - Script to run both backend and frontend in a single container

# Start the FastAPI backend in the background on port 8000
echo "Starting FastAPI Backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for the backend to start
sleep 3

# Start the Streamlit frontend on port 7860 (Hugging Face Spaces default port)
echo "Starting Streamlit Frontend..."
streamlit run frontend/app.py --server.port=7860 --server.address=0.0.0.0
