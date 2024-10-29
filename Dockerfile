    ################################
    # PYTHON-BASE
    ################################
    FROM python:3.12-slim as python-base

    # Python environment configuration
    ENV PYTHONDONTWRITEBYTECODE=1 \
        PYTHONUNBUFFERED=1 \
        POETRY_VERSION=1.8.4 \
        POETRY_HOME="/opt/poetry" \
        POETRY_NO_INTERACTION=1 \
        POETRY_VIRTUALENVS_CREATE=false \
        VIRTUAL_ENV="/venv"

    ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

    # Working directory and Python path setup
    WORKDIR /app
    ENV PYTHONPATH="/app:$PYTHONPATH"

    ################################
    # BUILDER-BASE
    ################################
    FROM python-base as builder-base
    RUN apt-get update && apt-get install -y \
        build-essential \
        curl \
        --no-install-recommends && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*

    RUN --mount=type=cache,target=/root/.cache \
        curl -sSL https://install.python-poetry.org | python3 -

    COPY poetry.lock pyproject.toml ./
    RUN --mount=type=cache,target=/root/.cache \
        poetry install --no-root --only main

    COPY . ./

    ################################
    # PRODUCTION
    ################################
    FROM builder-base as prod
    EXPOSE 8000

    ################################
    # DEVELOPMENT
    ################################
    FROM builder-base as dev
    RUN --mount=type=cache,target=/root/.cache \
        poetry install --no-root
    EXPOSE 8000        