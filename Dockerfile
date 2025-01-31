# Use Python 3.9 as the base image
FROM python:3.9-slim

# Install system dependencies (required for FAISS and spaCy)
RUN apt-get update && apt-get install -y \
    gcc \          # Compiler for some Python packages
    g++ \          # Compiler for C/C++ code
    libopenblas-dev \  # Math library for FAISS
    liblapack-dev \    # More math libraries
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy's English language model
RUN python -m spacy download en_core_web_sm

# Copy the rest of your code
COPY . .

# Command to run the app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
