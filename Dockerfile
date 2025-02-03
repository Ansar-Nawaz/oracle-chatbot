# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies globally
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train Rasa model
RUN rasa train --quiet --augmentation 0

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app

# Set PATH to include Python binaries
ENV PATH="/usr/local/bin:${PATH}"

# Railway configuration
ENV PORT=5005
EXPOSE $PORT

CMD rasa run --enable-api --cors "*" --port $PORT
