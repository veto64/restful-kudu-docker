#!/bin/bash
set -e

cd /opt/api
exec gunicorn --reload -b 0.0.0.0:80  main:api

