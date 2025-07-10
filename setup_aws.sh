#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker

# Install required fonts
sudo apt install -y fonts-freefont-ttf

# Create project directory
mkdir -p telegram-affiliate-bot/{src,config,fonts}
cd telegram-affiliate-bot

# Download Arial font
curl -o fonts/Arial.ttf https://raw.githubusercontent.com/googlefonts/roboto/main/src/hinted/Roboto-Regular.ttf

# Create config file
cat > config/.env <<EOL
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
PHONE=+1234567890
SOURCE_CHANNELS=@DealsChannel1,@DealsChannel2
DESTINATION_CONFIG=@Channel1:Watermark1;@Channel2:Watermark2
AMAZON_TAG=your_tag-20
FLIPKART_AFFID=your_flipkart_id
MYNTRA_PID=your_myntra_pid
EARNKARO_URL=https://earnkaro.com/page?url=
WATERMARK_FONT_SIZE=42
WATERMARK_COLOR=255,255,255
WATERMARK_POSITION=bottom-right
WATERMARK_MARGIN=25
EOL

echo "AWS setup complete. Edit config/.env with your credentials"