FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install with no cache to reduce image size
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Validate before training
RUN rasa data validate && rasa train

EXPOSE $PORT
CMD rasa run --enable-api --cors "*" --debug --port $PORT
