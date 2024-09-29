FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./alembic.ini /app/alembic.ini
COPY ./migration /app/migration
COPY ./models /app/models
COPY ./connection.py /app/connection.py

ENTRYPOINT ["alembic"]
