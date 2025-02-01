FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all your project files into the container
COPY . .

# Use Gunicorn to run the app; Railway provides the PORT environment variable.
CMD ["gunicorn", "main:app", "--workers", "3", "--bind", "0.0.0.0:$PORT"]




##FROM python:3.9-slim

##WORKDIR /app
##COPY . .

# Install dependencies (no PDF parsing/FAISS building)
##RUN pip install --upgrade pip && pip install --default-timeout=1000 -r requirements.txt
##RUN python -m spacy download en_core_web_sm

# Train Rasa
##RUN rasa train

#EXPOSE 5005
#CMD ["rasa", "run", "--enable-api", "--cors", "*"]
