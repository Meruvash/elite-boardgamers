# Radar Black no Railway (ver tools/black/railway/LEIAME.md)
FROM python:3.12-slim
RUN apt-get update -q && apt-get install -y -q --no-install-recommends git curl util-linux && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir requests Pillow beautifulsoup4 lxml feedparser price-parser protego cryptography boto3
WORKDIR /app
COPY . /app
ENV PYTHONUNBUFFERED=1 R2_PREFIXO=v2
CMD ["python3", "tools/black/railway/agendador.py"]
