FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train Rasa
RUN rasa train --quiet --augmentation 0

# Copy Python binaries explicitly
RUN cp -r /usr/local/lib/python3.9/site-packages/ /app/venv/
RUN cp /usr/local/bin/rasa /app/venv/bin/

# Railway settings
ENV PORT=5000
EXPOSE $PORT

CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5000", "--endpoints", "endpoints.yml"]
