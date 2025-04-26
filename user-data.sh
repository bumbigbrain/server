#!/bin/bash
cat > /home/ubuntu/server/.env << 'EOF'
PRIMARY_DB_ENDPOINT=""
PRIMARY_DB_USER=postgres
PRIMARY_DB_PASSWORD=postgres
PRIMARY_DB_NAME=postgres
SECONDARY_DB_ENDPOINT=""
SECONDARY_DB_USER=postgres
SECONDARY_DB_PASSWORD=postgres
SECONDARY_DB_NAME=postgres
EOF

su - ubuntu -c 'cd /home/ubuntu/server && ./run.sh'
