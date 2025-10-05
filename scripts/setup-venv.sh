#!/bin/bash
set -e -o pipefail

if [[ "$#" != 1 ]]; then
    echo "usage: $0 requirements.txt" 1>&2
    exit 1
fi

declare -r requirements="$1"
shift

set -x

python -m venv .venv
echo ". $PWD/.venv/bin/activate" >> ~/.bashrc
. ~/.bashrc

python -m ensurepip --upgrade
python -m pip install --upgrade setuptools
python -m pip install --upgrade $(cat "${requirements}"  | cut -d= -f1 | tr '\n' ' ') && python -m pip freeze >"${requirements}.new"
# python -m pip install -r "${requirements}"
