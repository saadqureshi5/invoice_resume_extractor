FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY backend/requirements.txt backend/
COPY frontend/requirements.txt frontend/
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN pip install --no-cache-dir -r frontend/requirements.txt

# Copy all project files
COPY . .

# Set up Python path so backend modules can be found
ENV PYTHONPATH=/app
# Hugging Face runs Streamlit on 7860
ENV PORT=7860
# Frontend will talk to the backend internally on 8000
ENV API_URL=http://localhost:8000

# Make start script executable
RUN chmod +x start.sh

# Expose ports (7860 for Streamlit, 8000 for FastAPI)
EXPOSE 7860
EXPOSE 8000

# Run the unified start script
CMD ["./start.sh"]
