# syntax=docker/dockerfile:1
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

RUN mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles

FROM base AS final
ENV DJANGO_COLLECTSTATIC=1
EXPOSE 8000

RUN addgroup --system django && adduser --system --ingroup django django

# important: give ownership
RUN chown -R django:django /app

# USER django
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "joblead.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
