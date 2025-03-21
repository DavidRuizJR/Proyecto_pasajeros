# pasajeros/Dockerfile
FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP pasajeros_app.py
ENV FLASK_RUN_PORT 5001
ENV DATABASE_URL postgresql://jdrt:traxi_prueba@pasajeros-db:5432/pasajeros
ENV RABBITMQ_URL 172.17.0.1


CMD ["flask", "run", "--host", "0.0.0.0"]

EXPOSE 5001