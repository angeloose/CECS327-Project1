# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /project1

# Copy necessary files
COPY master.py .
COPY node.py .

# Default command (will be overridden in compose.yaml)
CMD ["python3", "node.py"]