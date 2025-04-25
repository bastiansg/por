FROM por-core

COPY por /src/por
COPY requirements.txt pyproject.toml  /src/
RUN --mount=type=bind,source=.git,target=/src/.git \
    uv pip install /src --no-deps --system

WORKDIR /src/por/app
CMD python -m por.app.app
