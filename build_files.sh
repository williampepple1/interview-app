#!/bin/bash

echo "🔧 Starting Django build process..."

# Add Python bin to PATH
export PATH="/python312/bin:$PATH"

# Create static directories
mkdir -p static/css static/js static/images

# Install Python dependencies
python3 -m pip install --no-warn-script-location -r requirements.txt

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

echo "✅ Django build process completed."
