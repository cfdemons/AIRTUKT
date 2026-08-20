#!/usr/bin/env bash

set -e

echo "======================================"
echo "       AIRTUK Installation"
echo "======================================"

# --------------------------------------------------
<<<<<<< HEAD
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
=======
# 1. Check for Python 3.10
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace
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
<<<<<<< HEAD
# 3. Create virtual environment
=======
# 2. Create virtual environment
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace
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
<<<<<<< HEAD
# 4. Activate virtual environment
=======
# 3. Activate virtual environment
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace
# --------------------------------------------------

echo ""
echo "Activating virtual environment..."

<<<<<<< HEAD
source "$VENV_DIR"/bin/activate
=======
source "$VENV_DIR/bin/activate"
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace

echo "Active Python:"
python --version

# --------------------------------------------------
<<<<<<< HEAD
# 5. Upgrade pip
=======
# 4. Upgrade pip
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace
# --------------------------------------------------

echo ""
echo "Upgrading pip..."

python -m pip install --upgrade pip

# --------------------------------------------------
<<<<<<< HEAD
=======
# 5. Clean previous AIRTUK installtion (if any)
# --------------------------------------------------
python -m pip uninstall -y airtuk
rm -rf src/airtuk.egg-info

# --------------------------------------------------
>>>>>>> fbfaa3e02ad2daade2605d25bc7fe288e87b8ace
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


