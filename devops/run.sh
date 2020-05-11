#!/bin/sh
source venv/bin/activate
export DATABASE_URL=postgresql://username:password@postgres:5432/database_name
export APP_SETTINGS="config.DevelopmentConfig"

exec gunicorn -b :5000 --workers=1 --access-logfile - --error-logfile - app:app
