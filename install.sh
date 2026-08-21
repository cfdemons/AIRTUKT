#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUK Installation"
echo "======================================"

# --------------------------------------------------
# 1. Clean previous AIRTUK installtion (if any)
# --------------------------------------------------
echo ""
echo "Checking for previous AIRTUK installation..."

if [ -d ".buildenv" ] || \
   [ -d "src/airtuk.egg-info" ] || \
   compgen -G "$HOME/.airtuk/envs/airtuk*" > /dev/null 2>&1; then

    echo "Previous AIRTUK installation found."
    echo "Running uninstall.sh..."

    ./uninstall.sh
else
    echo "No previous AIRTUK installation found."
fi

# --------------------------------------------------
# 2. Check for Python 3.10
# --------------------------------------------------

if ! command -v python3.10 >/dev/null 2>&1; then
    echo ""
    echo "ERROR: AIRTUK requires Python 3.10"
    echo "Python 3.10 was not found on this system."
    echo ""
    exit 1
fi

echo ""
echo "Python 3.10 found:"
python3.10 --version

# --------------------------------------------------
# 3. Create virtual environment
# --------------------------------------------------

VENV_DIR=".buildenv"

if [ -d "$VENV_DIR" ]; then
    echo ""
    echo "Virtual environment '$VENV_DIR' already exists."
else
    echo ""
    echo "Creating virtual environment '$VENV_DIR'..."
    python3.10 -m venv "$VENV_DIR"

    echo "Virtual environment created."
fi

# --------------------------------------------------
# 4. Activate virtual environment
# --------------------------------------------------

echo ""
echo "Activating virtual environment..."

source "$VENV_DIR"/bin/activate

echo "Active Python:"
python --version

# --------------------------------------------------
# 5. Upgrade pip
# --------------------------------------------------

echo ""
echo "Upgrading pip..."

python -m pip install --upgrade pip

# --------------------------------------------------
# 5. Clean previous AIRTUK installtion (if any)
# --------------------------------------------------
python -m pip uninstall -y airtuk
rm -rf src/airtuk.egg-info

# --------------------------------------------------
# 6. Install AIRTUK
# --------------------------------------------------
echo ""
echo "Installing AIRTUK..."

python -m pip install -e .

# --------------------------------------------------
# 6. Install AIRTUK environments and kernels
# --------------------------------------------------

echo ""
echo "======================================"
echo "       Setting up AIRTUK environments"
echo "======================================"
echo ""

airtuk install


