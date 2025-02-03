# Stage 1: Build and train
FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Install minimal dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    rasa==3.6.15 \
    sentence-transformers==2.2.2 \
    faiss-cpu==1.7.4 \
    pandas==1.5.3 \
    spacy==3.7.4 && \
    python -m spacy download en_core_web_sm

# Train with minimal resources
RUN rasa train --quiet --augmentation 0

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app

# Railway-specific settings
ENV PORT=5005
EXPOSE $PORT

CMD rasa run --enable-api --cors "*" --port $PORT
