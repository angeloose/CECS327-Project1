Refer to pdf for instructions

Run commands:

# Build image
docker build -t ("image name) .

# Build & Start Containers
docker compose -t "(any name)" .

# Check running containers
docker ps

# Run individual dockerfile
docker run "(file name)"

# Build docker compose file
docker-compose build

# Run docker compose file
docker compose up

# Send test messages
docker exec -it node_a1 python3 /app/node.py

# Monitor Network traffic
docker exec -it cluster_a_master python3 /app/monitor.py


# misc notes for making project
You can edit code files (.py or compose.yaml) and the changes will be saved for running containers. Just make sure to 
1. docker-compose build   ->  2. docker-compose up

Rn monitor.pt and network.py not being used yet. Maybe somehow make it so only need master and node?
