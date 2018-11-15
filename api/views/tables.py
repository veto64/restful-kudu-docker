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
      'method' : 'get',
      'tables': []
    }

    table_name = 'master_foo'
    client = kudu.connect(host='queen', port=7051)
    print('xxxxxxxxxxxxxxxxxxxxxxxxx')
    print(client)
    print('xxxxxxxxxxxxxxxxxxxxxxxxx')
    api['tables'] = client.list_tables()

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200


  def on_delete(self, req, res):
    api = {
      '_API' : 'tables',
      'method' : 'delete',
      'result': []
    }  
