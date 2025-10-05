#!/bin/bash

. "${HOME}/.local/bin/env"

if [[ -f $1 && $(realpath "$1") =~ ^/app/repeater_roundabout/scripts/.*\.py$ ]]; then
    exec uv run "$@"
else
    exec "$@"
fi
