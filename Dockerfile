FROM python:3.10-slim

WORKDIR /rembg

RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip
RUN pip install ".[cpu,cli]" flask

COPY server.py server.py

EXPOSE 8080

CMD ["python", "server.py"]
