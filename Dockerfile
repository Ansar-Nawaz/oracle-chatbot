FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train Rasa
RUN rasa train --quiet --augmentation 0

# Runtime stage
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app

# Railway settings
ENV PORT=5000
EXPOSE $PORT

CMD rasa run --enable-api --cors "*" --port $PORT --endpoints endpoints.yml
