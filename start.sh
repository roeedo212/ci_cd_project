#!/bin/sh
python -c "from app import create_all; create_all()"
exec gunicorn -b 0.0.0.0:5000 app:app
