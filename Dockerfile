# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /CECS327-Project1

# Copy the script into the container
COPY network.py .

# Run the script when the container starts in terminal: "python network.py"
CMD ["python", "network.py"]