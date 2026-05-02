FROM por-core

COPY src/por /src/src/por
COPY requirements.txt pyproject.toml /src/
RUN --mount=type=bind,target=/root/.cache,source=.git,target=/src/.git \
    uv pip install /src --no-deps

WORKDIR /src
CMD python -m por.app.app
