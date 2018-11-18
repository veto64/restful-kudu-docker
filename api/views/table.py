#!/usr/bin/env python
import time
import falcon
import json
import kudu
from kudu.client import Partitioning
from datetime import datetime

class Table:

  def __init__(self,config):
   self.config = config
   self.api = {
      '_API'   : 'table',
      'method' : 'none',
      'table'  : 'none',
      'exists' :  False
    }

  def on_get(self, req, res,table):
    self.api['method'] = 'GET'
    self.api['table'] = table
    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)

    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200



  def on_put(self, req, res,table):
    self.api['method'] = 'PUT'
    self.api['table'] = table
    self.api['created'] = False
    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)

    if not self.api['exists']: 
      builder = kudu.schema_builder()
      #builder.add_column('id').type(kudu.int64).nullable(False).primary_key()
      builder.add_column('id').type(kudu.string).nullable(False).primary_key()
      schema = builder.build()
      partitioning = Partitioning().add_hash_partitions(column_names=['id'], num_buckets=3) 
      client.create_table(table, schema, partitioning)  
      self.api['created'] = True

    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200


  def on_delete(self, req, res,table):
    self.api['method'] = 'DELELTE'
    self.api['table'] = table
    self.api['deleted'] = False
    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)
    print(dir(client))

    if self.api['exists']: 
      client.delete_table(table)
      self.api['deleted'] = True

    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200

