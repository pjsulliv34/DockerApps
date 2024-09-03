# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy requirements file and install dependencies
COPY webapp/requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3.9-slim AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Copy the application code
COPY webapp /app/webapp

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=webapp/app.py

# Expose the port that the application will run on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "webapp.app:app"]
