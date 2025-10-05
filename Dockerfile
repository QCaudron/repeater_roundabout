FROM python:3.13-bookworm

ENV UID=1000
ENV GID=1000

ENV DEBIAN_FRONTEND=noninteractive

RUN groupadd --gid ${GID} app && \
    useradd --uid ${UID} --gid ${GID} -m --home /app app && \
    install -d -o ${UID} -g ${GID} /app/repeater_roundabout

RUN apt-get update && apt-get install -y --no-install-recommends \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/repeater_roundabout
USER app

COPY --chown=${UID}:${GID} ./requirements.txt /app/repeater_roundabout
COPY --chown=${UID}:${GID} ./scripts/setup-venv.sh /app/repeater_roundabout/scripts/setup-venv.sh
RUN cd /app \
    && repeater_roundabout/scripts/setup-venv.sh /app/repeater_roundabout/requirements.txt
RUN cp requirements.txt.new /tmp/

COPY --chown=${UID}:${GID} . /app/repeater_roundabout

ENTRYPOINT [ "/app/repeater_roundabout/scripts/docker-entrypoint.sh" ]
CMD [ "/bin/bash" ]
