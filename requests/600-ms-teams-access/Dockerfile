FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

# Unbuffered output so device-code flow prints immediately.
ENV PYTHONUNBUFFERED=1

# Default entrypoint; docker-compose overrides per service.
CMD ["python", "smoke_test.py"]
