#!/bin/sh

# Run migrations
python -m migrations.runner upgrade head

# Run server
python /opt/src/main.py &

# Start script for payments once a day in background
python /opt/src/payment.py &

exec "$@"
