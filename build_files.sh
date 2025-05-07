#!/bin/bash

echo "🔧 Starting Django build process..."

# Install Python dependencies
python3 -m pip install -r requirements.txt

# Run migrations
python3 manage.py migrate

# Collect static files
python3 manage.py collectstatic --noinput

echo "✅ Django build process completed."
