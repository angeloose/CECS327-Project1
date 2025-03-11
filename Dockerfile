FROM python:3.9

WORKDIR /app


RUN apt-get update && apt-get install -y tcpdump && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN pip install --no-cache-dir flask requests

# Copy necessary files
COPY network.py .
COPY master.py .
COPY node.py .
COPY monitor.py .

CMD ["python3", "network.py"]
