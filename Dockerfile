# Use a production-grade Rasa image (you can fix the version if needed)
FROM rasa/rasa:latest-full

# Set the working directory
WORKDIR /app

# Copy the entire project into the container
COPY . /app

# Upgrade pip and install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Download the small English model for spaCy (if using spaCy in your pipeline)
RUN python -m spacy download en_core_web_sm

# (Optional) Clean up any cache files if desired:
RUN rm -rf /root/.cache/pip

# Expose the port provided by Railway (Railway sets the PORT environment variable)
EXPOSE $PORT

# Start the Rasa server (using the pre-trained model from the models/ folder)
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug", "--port", "$PORT"]

