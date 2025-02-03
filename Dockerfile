# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /app
COPY . .

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Install Python dependencies globally (fixes PATH issues)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_sm

# Train Rasa
RUN rasa train --quiet --augmentation 0

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /home/appuser/.local /home/appuser/.local

# Add user's Python binaries to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Railway settings
ENV PORT=5005
EXPOSE $PORT

# Run as non-root user
USER appuser
CMD rasa run --enable-api --cors "*" --port $PORT
