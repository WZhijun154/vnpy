#!/bin/sh
set -eu

cd /app
exec python start_webserver.py
