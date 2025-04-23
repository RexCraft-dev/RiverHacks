#!/bin/bash

# Move to script directory
cd "$(dirname "$0")"

# Activate virtual environment
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Run the fetch script
echo "[*] Running fetch_tables.py..."
python fetch_tables.py

echo "[✓] Finished running fetch_tables.py"
