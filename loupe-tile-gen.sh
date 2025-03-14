#!/bin/bash

# Check if an image file is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: ./loupe-tile-gen.sh <image_path>"
    exit 1
fi
# Define the virtual environment folder
VENV_DIR=".venv"

# Check if the virtual environment exists, create if missing
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Ensure required packages are installed
pip install -q --upgrade pip
pip install -q pillow python-resize-image

# Run the Python script with the provided image path
python3 loupe-tile-gen.py "$1"

# Deactivate the virtual environment
deactivate