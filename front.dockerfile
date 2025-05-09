# Build with all dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt update && apt install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY ./front/requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Final lightweight image
FROM python:3.12-slim

WORKDIR /app

# Install reflex dependencies
RUN apt update && apt install -y --no-install-recommends \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only the installed packages
COPY --from=builder /install /usr/local

# Copy the app
COPY front ./front

WORKDIR /app/front

# Run the reflex app with explicit host binding
CMD ["reflex", "run", "--backend-host", "0.0.0.0"]