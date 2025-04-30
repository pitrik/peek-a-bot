FROM python:3.11-slim

# Install certificates
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

# Install discord.py and aiohttp
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir "discord.py>=2.3.0" aiohttp

CMD ["python", "bot.py"]