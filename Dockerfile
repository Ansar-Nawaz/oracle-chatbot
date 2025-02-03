# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app

# Copy ALL required files from builder stage
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/rasa /usr/local/bin/rasa

# Railway settings
ENV PORT=5000
EXPOSE $PORT

# Use shell form to ensure ENV variables work
CMD rasa run --enable-api --cors "*" --port $PORT --endpoints endpoints.yml
