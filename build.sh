#!/usr/bin/env bash
# Render build script — runs on every deployment
set -o errexit

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🗂  Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄  Running database migrations..."
python manage.py migrate

echo "🌱 Seeding demo content..."
python manage.py seed_demo_data

echo "👤 Creating admin user (if not exists)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@naishacoffee.com', 'NaishaCoffee2024!')
    print('  Admin created → username: admin | password: NaishaCoffee2024!')
else:
    print('  Admin already exists.')
"

echo "✅ Build complete!"
