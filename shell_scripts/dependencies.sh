#!/bin/bash

# Set up virtual environment
echo "[*] Creating virtual environment..."
python3 -m venv venv

# Activate it
echo "[*] Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[*] Installing requirements..."
pip install -r requirements.txt

echo "[✓] Dependencies installed successfully."
