#syntax=docker/dockerfile:1.7-labs

ARG PYTHON_VERSION=3.12
ARG NODE_VERSION=22

# Compile the JS code in a node container
FROM node:${NODE_VERSION} AS js
WORKDIR /app
COPY tasks/frontend/package.json tasks/frontend/yarn.lock /app/
RUN --mount=type=cache,target=/usr/local/share/.cache/yarn yarn install --frozen-lockfile
COPY tasks/frontend /app
RUN yarn build

# Build the python container
ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}
RUN useradd -s /bin/bash checkdown -m -d /app -U -u 1000
WORKDIR /app
USER checkdown
RUN python -m venv /app/.venv
COPY requirements.txt /app
RUN --mount=type=cache,target=/app/.cache/pip,uid=1000 bash -c "source /app/.venv/bin/activate && pip install -r requirements.txt"
COPY --chown=checkdown:checkdown --exclude=tasks/frontend . /app
RUN python -m compileall /app
COPY --from=js --link --chown=checkdown:checkdown /app/dist /app/tasks/frontend/dist
EXPOSE 8000
CMD ["bash", "-c", "source /app/.venv/bin/activate \
    && python manage.py check --deploy \
    && python manage.py migrate \
    && (python manage.py createsuperuser --noinput --email $DJANGO_SUPERUSER_EMAIL --username $DJANGO_SUPERUSER_USERNAME || true) \
    && hypercorn checkdown.asgi:application --bind 0.0.0.0:8000"]
