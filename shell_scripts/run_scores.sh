#!/bin/bash

# Move to the script's directory
cd "$(dirname "$0")"

# Activate the virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Run the scores script with arguments
echo "[*] Running scores.py with full export..."
python scores.py --file scores.csv --exportall

echo "[✓] Finished scoring and exporting results"
