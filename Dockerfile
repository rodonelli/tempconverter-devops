FROM python:3.12-slim

ARG IMAGE_VARIANT=dev
LABEL org.opencontainers.image.title="TempConverter" \
      org.opencontainers.image.description="Celsius to Fahrenheit web application" \
      org.opencontainers.image.version="${IMAGE_VARIANT}"

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system app \
    && useradd --system --gid app --create-home app

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app app.py ./
COPY --chown=app:app templates ./templates

USER app
EXPOSE 5000/tcp
HEALTHCHECK --interval=10s --timeout=3s --start-period=40s --retries=5 \
  CMD curl --fail http://127.0.0.1:5000/healthz || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "app:create_app()"]
