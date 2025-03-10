# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir flask requests scapy

# Copy necessary files
COPY network.py .
COPY master.py .
COPY node.py .
COPY monitor.py .

# Default command (will be overridden in compose.yaml)
CMD ["python3", "node.py"]