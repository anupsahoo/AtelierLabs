FROM python:3.11-slim AS base

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install --no-cache-dir .

COPY .env* ./
COPY src/autonomy_gatekeeper/policy/ src/autonomy_gatekeeper/policy/

ENTRYPOINT ["autonomy-gatekeeper"]
