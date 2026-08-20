#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUK Uninstallation"
echo "======================================"

VENV_DIR=".buildenv"

# --------------------------------------------------
# 1. Check for virtual environment
# --------------------------------------------------

if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "Virtual environment '$VENV_DIR' was not found."
else

    # --------------------------------------------------
    # 2. Activate virtual environment
    # --------------------------------------------------

    echo ""
    echo "Activating virtual environment..."

    source "$VENV_DIR/bin/activate"

    # --------------------------------------------------
    # 3. Uninstall AIRTUK Python package
    # --------------------------------------------------

    echo ""
    echo "Uninstalling AIRTUK Python package..."

    python -m pip uninstall -y airtuk || true

    deactivate
fi

# --------------------------------------------------
# 4. Remove AIRTUK package metadata
# --------------------------------------------------

echo ""
echo "Removing AIRTUK build metadata..."

rm -rf src/airtuk.egg-info

# --------------------------------------------------
# 5. Remove AIRTUK environments
# --------------------------------------------------

echo ""
echo "Removing AIRTUK environments..."

rm -rf "$HOME"/.airtuk/envs/airtuk*

# --------------------------------------------------
# 6. Remove virtual environment
# --------------------------------------------------

if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Removing virtual environment '$VENV_DIR'..."
    rm -rf "$VENV_DIR"
fi

# --------------------------------------------------
# 7. Done
# --------------------------------------------------

echo ""
echo "======================================"
echo "       AIRTUK Uninstallation Complete"
echo "======================================"
echo ""
