#!/usr/bin/env bash

set -e

VENV_DIR=".buildenv"
PYTHON="$VENV_DIR/bin/python"
AIRTUK="$VENV_DIR/bin/airtuk"

# --------------------------------------------------
# 1. Check AIRTUK environment
# --------------------------------------------------

if [ ! -x "$PYTHON" ] || [ ! -x "$AIRTUK" ]; then
    echo ""
    echo "ERROR: AIRTUK environment was not found."
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
echo "AIRTUK Python:"
"$PYTHON" --version

# --------------------------------------------------
# 3. Launch AIRTUK
# --------------------------------------------------

echo ""
echo "======================================"
echo "       Launching AIRTUK"
echo "======================================"
echo ""

exec "$AIRTUK" notebook
