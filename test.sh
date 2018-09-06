#!/bin/bash
docker run --network=kududocker_queen  --rm -v "`pwd`:/opt/test"  veto64/kudu-docker /usr/bin/python /opt/test/main.py
