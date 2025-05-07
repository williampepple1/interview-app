#!/bin/bash

echo "🔧 Starting Django build process..."

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

echo "✅ Django build process completed."
