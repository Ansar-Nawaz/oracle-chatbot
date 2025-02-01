FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN rasa train
EXPOSE $PORT
CMD rasa run --enable-api --cors "*" --debug --port $PORT
