#!/bin/bash

# Build and run the Docker container
docker build -t affiliate-bot .
docker run -d \
  --restart always \
  --name affiliate-bot \
  -v $(pwd)/config/.env:/app/config/.env \
  affiliate-bot

# Show logs
echo "Container started. Showing logs:"
docker logs -f affiliate-bot