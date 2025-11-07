# ----------------------------------------------------------
# Autonomous Data Quality Guardian - Dockerfile
# ----------------------------------------------------------
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . /app

# Install system packages needed for psycopg2, SSL & GE
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    ca-certificates \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip & install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install python-certifi-win32

# Expose Streamlit dashboard port
EXPOSE 8501

# Default: run the main Guardian pipeline
CMD ["python", "main.py"]
