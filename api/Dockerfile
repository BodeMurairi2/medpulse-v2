# Use Python slim image
FROM python:3.11-slim

# Install system dependencies including PostgreSQL client
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY . .

# Expose backend port (change if needed)
EXPOSE 8080

# Set default command to run your wait-for-db script (adjust if your entrypoint differs)
CMD ["./wait-for-db.sh", "db", "uvicorn", "web.web:app", "--host", "0.0.0.0", "--port", "8080"]
