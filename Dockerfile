FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install with minimal memory footprint
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Suppress TensorFlow logs
ENV TF_CPP_MIN_LOG_LEVEL=3

# Train with reduced resources (disable augmentation)
RUN rasa train --quiet --augmentation 0

EXPOSE $PORT
CMD rasa run --enable-api --cors "*" --port $PORT
