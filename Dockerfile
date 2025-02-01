FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install with minimal memory footprint
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train with reduced resources
ENV TF_CPP_MIN_LOG_LEVEL=3  # Suppress TensorFlow logs
RUN rasa train --quiet --augmentation 0  # Disable augmentation

EXPOSE $PORT
CMD rasa run --enable-api --cors "*" --port $PORT
