#!/bin/bash
set -e  # Exit on any error

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Verifying streamlit installation..."
which streamlit

echo "Build complete!"
