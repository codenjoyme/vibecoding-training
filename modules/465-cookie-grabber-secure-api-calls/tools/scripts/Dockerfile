FROM python:3.12-slim

WORKDIR /app

COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

COPY server.py .
COPY extension/ ./extension/

RUN mkdir -p /data

EXPOSE 9011

CMD ["python", "server.py"]
