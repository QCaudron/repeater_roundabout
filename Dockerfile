FROM python:3.12-bookworm

ENV UID=1000
ENV GID=1000
ENV UV_VERSION=0.8.23

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd --gid ${GID} app && \
    useradd --uid ${UID} --gid ${GID} -m --home /app app && \
    install -d -o ${UID} -g ${GID} /app/repeater_roundabout

RUN apt-get update && apt-get install -y --no-install-recommends \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/repeater_roundabout
USER app

RUN curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh

COPY --chown=${UID}:${GID} ./pyproject.toml /app/repeater_roundabout/
RUN . $HOME/.local/bin/env && uv sync

COPY --chown=${UID}:${GID} . /app/repeater_roundabout/

ENTRYPOINT [ "/app/repeater_roundabout/scripts/docker-entrypoint.sh" ]
CMD [ "/bin/bash" ]
