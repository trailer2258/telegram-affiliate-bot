FROM python:3.9-slim-bullseye

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    fonts-freefont-ttf \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create font directory
RUN mkdir -p /usr/share/fonts/truetype/custom/
COPY fonts/Arial.ttf /usr/share/fonts/truetype/custom/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the bot
CMD ["python", "./src/affiliate_bot.py"]