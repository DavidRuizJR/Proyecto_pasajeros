FROM python:3.9-slim-buster

WORKDIR /app

COPY ./src/reservas/ ./

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP reservas_app.py
ENV FLASK_RUN_PORT 5000

CMD ["flask", "run", "--host", "0.0.0.0"]

EXPOSE 5000