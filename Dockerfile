FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY django_api_project/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY django_api_project/ .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
