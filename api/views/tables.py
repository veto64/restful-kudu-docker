#!/usr/bin/env python
import time
import falcon
import json
import kudu
from kudu.client import Partitioning
from datetime import datetime

class Tables:

  def __init__(self,config):
   self.config = config

  def on_get(self, req, res):
    api = {
      '_API' : 'tables',
      'tables': []
    }

    table_name = 'master_foo'
    client = kudu.connect(host='queen', port=7051)
    api['tables'] = client.list_tables()

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200
