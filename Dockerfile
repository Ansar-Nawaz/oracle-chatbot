FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install with strict versions
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    rasa==3.6.15 \
    sentence-transformers==2.2.2 \
    faiss-cpu==1.7.4 \
    pandas==2.0.3 \
    spacy==3.7.4

# Download model and validate
RUN python -m spacy download en_core_web_sm && \
    rasa data validate

# Train
RUN rasa train --quiet

EXPOSE $PORT
CMD rasa run --enable-api --cors "*" --port $PORT
