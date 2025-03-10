Refer to pdf for instructions

Run commands:
# Build & Start Containers
docker compose -t "(any name)" .

# Check running containers
docker ps\

# Run docker compose file
docker compose up

# Send test messages
docker exec -it node_a1 python3 /app/node.py

# Monitor Network traffic
docker exec -it cluster_a_master python3 /app/monitor.py