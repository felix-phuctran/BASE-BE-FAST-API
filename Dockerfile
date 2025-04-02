# Stage 1: Build
FROM python:3.10.14-slim AS builder

# Set the working directory
WORKDIR /app

# Install required build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt uvicorn[standard]

# Stage 2: Runtime
FROM python:3.10.14-slim

# Set the working directory
WORKDIR /app

# Install minimal runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy dependencies and application code
COPY --from=builder /root/.local /root/.local
COPY app /app/app
COPY shared /app/shared
COPY alembic /app/alembic
COPY alembic.ini /app/alembic.ini

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/root/.local/bin:$PATH"

# Expose port
EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]
