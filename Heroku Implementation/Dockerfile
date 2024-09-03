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

# Copy the application code
COPY . .

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV FLASK_APP=app.py

# Expose the port that the application will run on
EXPOSE 5000
CMD ["python", "-m" , "flask", "run", "--host=0.0.0.0"]