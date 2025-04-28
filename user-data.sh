#!/bin/bash

set -e  # Exit on any error

# Update and install packages as root
apt update -y
apt upgrade -y
apt install python3-venv uvicorn stress-ng git -y

# Clone repository as ubuntu user
su - ubuntu -c 'cd /home/ubuntu/ && git clone https://github.com/bumbigbrain/server.git'

# Create .env file
cat > /home/ubuntu/server/.env << 'EOF'
PRIMARY_DB_ENDPOINT=""
PRIMARY_DB_USER=postgres
PRIMARY_DB_PASSWORD=postgres
PRIMARY_DB_NAME=postgres

SECONDARY_DB_ENDPOINT=""
SECONDARY_DB_USER=postgres
SECONDARY_DB_PASSWORD=postgres
SECONDARY_DB_NAME=postgres

MINIO_ENDPOINT=""
MINIO_PORT=9001
MINIO_ACCESS_KEY=""
MINIO_SECRET_KEY=""
EOF

# Set permissions
chown ubuntu:ubuntu /home/ubuntu/server/.env
chmod +x /home/ubuntu/server/setup.sh
chmod +x /home/ubuntu/server/run.sh

# Run setup and start application as ubuntu user
su - ubuntu -c 'cd /home/ubuntu/server && ./setup.sh && ./run.sh'
