FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN chmod +x /app/entrypoint.sh

# Collect static files (run as root before switching user)
RUN python manage.py collectstatic --noinput || true

ENV PORT=80
EXPOSE 80

ENTRYPOINT ["/app/entrypoint.sh"]