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
   self.api = {
      '_API' : 'tables',
      'method' : '',
      'tables': {}
    }

  def on_get(self, req, res):
    self.api['method'] = 'GET'
    client = kudu.connect(host='queen', port=7051)
    tables = client.list_tables()
    for i in tables:
      table = client.table(i)
      self.api['tables'][i] = str(table.schema)
    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200


  def on_delete(self, req, res):
    self.api['method'] = 'DELETE'
