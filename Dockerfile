# syntax=docker/dockerfile:1

FROM node:22-bookworm-slim AS base

WORKDIR /app

ENV NPM_CONFIG_UPDATE_NOTIFIER=false

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
  && rm -rf /var/lib/apt/lists/*

FROM base AS deps

COPY package.json package-lock.json ./
RUN npm ci

COPY requirements.txt requirements-dev.txt ./
RUN python3 -m venv .venv \
  && .venv/bin/python -m pip install --upgrade pip \
  && .venv/bin/pip install -r requirements-dev.txt

FROM deps AS build

ENV PATH="/app/.venv/bin:${PATH}"

COPY . .

RUN python -m pytest
RUN python -m ruff check .
RUN python -m mypy scripts tests
RUN python scripts/validate_assets.py
RUN python scripts/validate_content_sources.py
RUN npm run build

FROM nginx:1.27-alpine AS runtime

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
