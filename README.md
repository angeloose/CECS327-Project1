Refer to pdf for instructions

Run commands:
# Build & Start Containers
docker-compose up --build

# Check running containers
docker ps

# Send test messages
docker exec -it node_a1 python3 /app/node.py

# Monitor Network traffic
docker exec -it cluster_a_master python3 /app/monitor.py