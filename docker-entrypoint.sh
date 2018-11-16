#!/bin/bash
set -e
cd /opt/api
exec gunicorn --reload --access-logfile api.log --log-level debug  -b 0.0.0.0:80  main:api

