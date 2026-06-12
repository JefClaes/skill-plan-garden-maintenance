#!/usr/bin/env bash
# Convenience runner: set up a venv (first run), install deps, run the test suite.
# Works under Git Bash on Windows and on macOS/Linux. Passes any extra args to pytest.
#
#   ./run-tests.sh                      # full suite
#   ./run-tests.sh tests/test_schema.py # structural checks only
#   ./run-tests.sh -m llm -k timing     # forward any pytest args
#
# Reads ANTHROPIC_API_KEY / GENERATION_MODEL / JUDGE_MODEL from .env (via the tests'
# python-dotenv). With no API key the suite skips cleanly instead of failing.

set -euo pipefail
cd "$(dirname "$0")"

VENV=".venv"

# venv python lives in Scripts/ on Windows, bin/ elsewhere.
if [ -x "$VENV/Scripts/python.exe" ]; then
  PY="$VENV/Scripts/python.exe"
elif [ -x "$VENV/bin/python" ]; then
  PY="$VENV/bin/python"
else
  PY=""
fi

if [ -z "$PY" ]; then
  echo "==> Creating virtual environment in $VENV"
  python -m venv "$VENV"
  if [ -x "$VENV/Scripts/python.exe" ]; then
    PY="$VENV/Scripts/python.exe"
  else
    PY="$VENV/bin/python"
  fi
  echo "==> Installing dependencies"
  "$PY" -m pip install --quiet --upgrade pip
  "$PY" -m pip install --quiet -e .
fi

if [ ! -f .env ]; then
  echo "WARNING: no .env found. Copy .env.example to .env and set ANTHROPIC_API_KEY"
  echo "         to run the live tests. Without a key the suite will skip them."
fi

echo "==> Running pytest"
exec "$PY" -m pytest "$@"
