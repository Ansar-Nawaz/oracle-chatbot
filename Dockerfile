# Use an official Python image that supports virtual environments
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install OS-level dependencies that might be needed for building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy your project files into the container
COPY . /app/

# (Optional) Set an environment variable if needed
ENV NIXPACKS_PATH=/opt/venv/bin:$NIXPACKS_PATH

# Create a virtual environment, activate it, upgrade pip, and install dependencies.
RUN python -m venv --copies /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port your app is running on (change if needed)
EXPOSE 5000

# Start your application using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

