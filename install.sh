#!/bin/bash
set -e

echo "Installing Oldy..."

# Check Python 3.10+
python3 --version | grep -E "3\.(1[0-9])" > /dev/null 2>&1 || {
    echo "Error: Python 3.10 or higher is required."
    exit 1
}

# Install oldy via pip
pip3 install oldy --quiet

echo ""
echo "Oldy installed. Run: oldy start"
