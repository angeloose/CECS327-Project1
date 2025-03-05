# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the script into the container
COPY app.py .

# Run the script when the container starts
CMD ["python", "network.py"]