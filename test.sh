#!/bin/bash
docker run --network=kudu-docker_queen  --rm -v "`pwd`:/opt/test"  veto64/kudu-docker /usr/bin/python /opt/test/main.py
