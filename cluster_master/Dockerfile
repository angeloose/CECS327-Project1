# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy necessary files
COPY requirements.txt requirements.txt
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command (will be overridden in compose.yaml)
CMD ["python3", "node.py"]
