#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
exec .venv/bin/python runner.py stop
