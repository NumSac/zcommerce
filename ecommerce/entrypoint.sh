#!/bin/sh

# Wait for database to be ready
# Uncomment and modify the next lines if your Django app requires a database
# echo "Waiting for postgres..."
# while ! nc -z $SQL_HOST $SQL_PORT; do
#   sleep 0.1
# done
# echo "PostgreSQL started"

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

echo "Applying Subscription group migrations"
python manage.py create_subscription_groups

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8001
