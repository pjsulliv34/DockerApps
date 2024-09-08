# Stage 1: Builder
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runner
FROM python:3.9-slim AS runner

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Copy the application code from the current directory
COPY . /app

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app.py

# Set OpenAI API Key using a build argument
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
# Expose the port that the application will run on
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
