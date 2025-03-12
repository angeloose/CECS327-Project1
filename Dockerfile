# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /project1

# Install tcpdump
RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*

# Copy necessary files
COPY master.py .
COPY node.py .

# Default command (will be overridden in compose.yaml)
CMD ["python3", "node.py"]