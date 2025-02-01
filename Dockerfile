FROM python:3.9-slim

WORKDIR /app
COPY . .

# Install dependencies (no PDF parsing/FAISS building)
RUN pip install --upgrade pip && pip install --default-timeout=1000 -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Train Rasa
RUN rasa train

EXPOSE 5005
CMD ["rasa", "run", "--enable-api", "--cors", "*"]
