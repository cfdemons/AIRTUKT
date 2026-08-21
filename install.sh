#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUK Installation"
echo "======================================"

# --------------------------------------------------
# Configuration
# --------------------------------------------------

VENV_DIR=".buildenv"
PYTHON_VERSION="3.10"

# --------------------------------------------------
# 1. Clean previous AIRTUK installation (if any)
# --------------------------------------------------

echo ""
echo "Checking for previous AIRTUK installation..."

if [ -d "$VENV_DIR" ] || \
   [ -d "src/airtuk.egg-info" ] || \
   compgen -G "$HOME/.airtuk/envs/airtuk*" > /dev/null 2>&1; then

    echo "Previous AIRTUK installation found."
    echo "Running uninstall.sh..."

    ./uninstall.sh
else
    echo "No previous AIRTUK installation found."
fi

# --------------------------------------------------
# 2. Install uv if necessary
# --------------------------------------------------

echo ""
echo "Checking for uv..."

if command -v uv >/dev/null 2>&1; then
    echo "uv found:"
    uv --version
else
    echo "uv not found."
    echo "Installing uv..."

    curl -LsSf https://astral.sh/uv/install.sh | sh

    # uv normally installs here
    export PATH="$HOME/.local/bin:$PATH"

    if ! command -v uv >/dev/null 2>&1; then
        echo ""
        echo "ERROR: uv was installed but could not be found."
        echo "Please add ~/.local/bin to your PATH and run this installer again."
        exit 1
    fi

    echo "uv installed:"
    uv --version
fi

# --------------------------------------------------
# 3. Install Python 3.10 using uv
# --------------------------------------------------

echo ""
echo "Checking for Python $PYTHON_VERSION..."

echo "Ensuring Python $PYTHON_VERSION is available through uv..."

uv python install "$PYTHON_VERSION"

echo ""
echo "Python $PYTHON_VERSION:"
uv run --python "$PYTHON_VERSION" python --version

# --------------------------------------------------
# 4. Create virtual environment
# --------------------------------------------------

if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Virtual environment '$VENV_DIR' already exists."
else
    echo ""
    echo "Creating virtual environment '$VENV_DIR' with Python $PYTHON_VERSION..."

    uv venv "$VENV_DIR" --python "$PYTHON_VERSION"

    echo "Virtual environment created."
fi

# --------------------------------------------------
# 5. Verify virtual environment
# --------------------------------------------------

PYTHON="$VENV_DIR/bin/python"
PIP="$VENV_DIR/bin/pip"
AIRTUK="$VENV_DIR/bin/airtuk"

echo ""
echo "Virtual environment Python:"
"$PYTHON" --version

# --------------------------------------------------
# 6. Upgrade pip
# --------------------------------------------------

echo ""
echo "Upgrading pip..."

uv pip install \
    --python "$PYTHON" \
    --upgrade pip

# --------------------------------------------------
# 7. Install AIRTUK
# --------------------------------------------------

echo ""
echo "Installing AIRTUK..."

uv pip install \
    --python "$PYTHON" \
    -e .

# --------------------------------------------------
# 8. Install AIRTUK environments and kernels
# --------------------------------------------------

echo ""
echo "======================================"
echo "       Setting up AIRTUK environments"
echo "======================================"
echo ""

"$AIRTUK" install

echo ""
echo "======================================"
echo "       AIRTUK Installation Complete"
echo "======================================"
echo ""
echo "Python: $("$PYTHON" --version)"
echo "Environment: $VENV_DIR"
echo ""
          

                                                             
