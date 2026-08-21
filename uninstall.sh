#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUK Uninstallation"
echo "======================================"

VENV_DIR=".buildenv"
PYTHON="$VENV_DIR/bin/python"

# --------------------------------------------------
# 1. Check for virtual environment
# --------------------------------------------------

if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Virtual environment '$VENV_DIR' was not found."
else

    # --------------------------------------------------
    # 2. Uninstall AIRTUK Python package
    # --------------------------------------------------

    echo ""
    echo "Uninstalling AIRTUK Python package..."

    if [ -x "$PYTHON" ]; then
        "$PYTHON" -m pip uninstall -y airtuk || true
    else
        echo "Python executable not found in '$VENV_DIR'."
        echo "Skipping Python package uninstall."
    fi
fi

# --------------------------------------------------
# 3. Remove AIRTUK package metadata
# --------------------------------------------------

echo ""
echo "Removing AIRTUK build metadata..."

rm -rf src/airtuk.egg-info

# --------------------------------------------------
# 4. Remove AIRTUK environments
# --------------------------------------------------

echo ""
echo "Removing AIRTUK environments..."

if compgen -G "$HOME/.airtuk/envs/airtuk*" > /dev/null 2>&1; then
    rm -rf "$HOME"/.airtuk/envs/airtuk*
    echo "AIRTUK environments removed."
else
    echo "No AIRTUK environments found."
fi

# --------------------------------------------------
# 5. Remove AIRTUK virtual environment
# --------------------------------------------------

if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Removing virtual environment '$VENV_DIR'..."
    rm -rf "$VENV_DIR"
    echo "Virtual environment removed."
fi

# --------------------------------------------------
# 6. Done
# --------------------------------------------------

echo ""
echo "======================================"
echo "       AIRTUK Uninstallation Complete"
echo "======================================"
echo ""
