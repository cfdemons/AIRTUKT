# --------------------------------------------------
# 1. Activate virtual environment
# --------------------------------------------------

echo ""
echo "Activating virtual environment..."

source ".buildenv/bin/activate"

echo "Active Python:"
python --version

# --------------------------------------------------
# 2. Launch Jupyter Notebook
# --------------------------------------------------

echo ""
echo "======================================"
echo "       Launching AIRTUK"
echo "======================================"
echo ""

airtuk notebook
