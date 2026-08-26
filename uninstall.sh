#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUKT Uninstallation"
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
    # 2. Uninstall AIRTUKT Python package
    # --------------------------------------------------

    echo ""
    echo "Uninstalling AIRTUKT Python package..."

    if [ -x "$PYTHON" ]; then
        "$PYTHON" -m pip uninstall -y airtukt || true
    else
        echo "Python executable not found in '$VENV_DIR'."
        echo "Skipping Python package uninstall."
    fi
fi

# --------------------------------------------------
# 3. Remove AIRTUKT package metadata
# --------------------------------------------------

echo ""
echo "Removing AIRTUKT build metadata..."

rm -rf src/airtukt.egg-info

# --------------------------------------------------
# 4. Remove AIRTUKT environments
# --------------------------------------------------

echo ""
echo "Removing AIRTUKT environments..."

if compgen -G "$HOME/.airtukt/envs/airtukt*" > /dev/null 2>&1; then
    rm -rf "$HOME"/.airtukt/envs/airtukt*
    echo "AIRTUKT environments removed."
else
    echo "No AIRTUKT environments found."
fi

# --------------------------------------------------
# 5. Remove AIRTUKT virtual environment
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
echo "       AIRTUKT Uninstallation Complete"
echo "======================================"
echo ""
