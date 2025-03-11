# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /project1

# Copy necessary files into /project1
COPY node.py .
COPY master.py .

# Install dependencies
RUN apt-get update && apt-get install -y tcpdump 
RUN pip install --no-cache-dir flask requests 

# Default command (will be overridden in compose.yaml)
CMD ["python3", "master.py"]
