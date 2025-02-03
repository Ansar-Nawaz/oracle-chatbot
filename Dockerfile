FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN apt-get update && apt-get install -y gcc && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

RUN rasa train --quiet

ENV PORT=5000
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5000", "--endpoints", "endpoints.yml"]
