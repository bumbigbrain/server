#!/bin/bash


su - ubuntu -c 'cd /home/ubuntu/ && git clone https://github.com/bumbigbrain/server.git'

cat > /home/ubuntu/server/.env << 'EOF'
PRIMARY_DB_ENDPOINT=""
PRIMARY_DB_USER=postgres
PRIMARY_DB_PASSWORD=postgres
PRIMARY_DB_NAME=postgres

SECONDARY_DB_ENDPOINT=""
SECONDARY_DB_USER=postgres
SECONDARY_DB_PASSWORD=postgres
SECONDARY_DB_NAME=postgres

MINIO_ENDPOINT=endpoint
MINIO_PORT=port
MINIO_ACCESS_KEY=access_key
MINIO_SECRET_KEY=secret_key
EOF

su - ubuntu -c 'cd /home/ubuntu/server && source setup.sh && ./run.sh'
