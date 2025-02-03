# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train the model
RUN rasa train --quiet --augmentation 0

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/rasa /usr/local/bin/rasa

# Railway settings
ENV PORT=5000
EXPOSE $PORT

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5000"]
