#!/usr/bin/env bash
set -o errexit

PYTHON=$(command -v python3 || command -v python)
PIP=$(command -v pip3 || command -v pip)

$PIP install -r requirements.txt

$PYTHON manage.py collectstatic --noinput

$PYTHON manage.py migrate