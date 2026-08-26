#!/usr/bin/env bash

set -e

VENV_DIR=".buildenv"
PYTHON="$VENV_DIR/bin/python"
AIRTUKT="$VENV_DIR/bin/airtukt"

# --------------------------------------------------
# 1. Check AIRTUKT environment
# --------------------------------------------------

if [ ! -x "$PYTHON" ] || [ ! -x "$AIRTUKT" ]; then
    echo ""
    echo "ERROR: AIRTUKT environment was not found."
    echo ""
    echo "Please run:"
    echo ""
    echo "    ./install.sh"
    echo ""
    exit 1
fi

# --------------------------------------------------
# 2. Show Python version
# --------------------------------------------------

echo ""
echo "AIRTUKT Python:"
"$PYTHON" --version

# --------------------------------------------------
# 3. Launch AIRTUKT
# --------------------------------------------------

echo ""
echo "======================================"
echo "       Launching AIRTUKT"
echo "======================================"
echo ""

exec "$AIRTUKT" notebook
