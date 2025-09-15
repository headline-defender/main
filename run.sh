#!/bin/sh
WORKERS=2
THREADS=2

exec gunicorn \
  --workers "$WORKERS" \
  --threads "$THREADS" \
  --bind 0.0.0.0:5000 \
  app:app
