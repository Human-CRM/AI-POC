# Build with all dependencies
FROM python:3.12-slim as builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY ./back/requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# Final lightweight image
FROM python:3.12-slim-bullseye

WORKDIR /app

# Copy only the installed packages
COPY --from=builder /install /usr/local

# Copy your app code
COPY back ./back
COPY basic_json ./apollo/organizations

CMD ["python", "back"]
