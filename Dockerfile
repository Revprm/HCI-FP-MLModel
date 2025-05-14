# --- builder stage: install dependencies ---
FROM python:3.13-slim-bookworm AS builder

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build tools
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc python3-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only requirements, so that Docker can cache this layer until requirements.txt changes
COPY requirements.txt .

# Install into a custom prefix (/install) so we can copy it later
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# --- final stage: runtime image ---
FROM python:3.13-slim-bookworm

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non‑root user
RUN groupadd -r appuser \
 && useradd -r -g appuser appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy your app code
COPY . .

# Ensure the app directory is owned by our non‑root user
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

# Launch Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
