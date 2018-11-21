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
      builder.add_column('id').type(kudu.int64).nullable(False).primary_key()
      schema = builder.build()
      partitioning = Partitioning().add_hash_partitions(column_names=['id'], num_buckets=3) 
      client.create_table(table, schema, partitioning)  
      self.api['created'] = True

    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200

  def on_update(self, req, res,table):
    self.api['method']  = 'UPDATE'
    self.api['table']   = table
    self.api['updated'] = False
    self.api['exists']  = False
    self.api['error']  = []

    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)
    if self.api['exists']:
      otable = client.table(table)
      alt = client.new_table_alterer(otable)
      self.api['name'] = req.get_param('name')
      self.api['data'] = json.load(req.bounded_stream)

      if self.api['data']:
        if 'cols' in self.api['data']:
          try:
            for i in self.api['data']['cols']:
              alt.alter_column(i,self.api['data']['cols'][i])
            alt.alter()
          except Exception as e:
            self.api['error'].append(str(e))

      if self.api['name']:
        try:
          t = alt.rename(self.api['rename']).alter()
        except Exception as e:
          self.api['error'].append(str(e))

      #alt.add_column('tests').type(kudu.string)
      #alt.alter()
      
      #self.api['log'] = str(dir(alt))

    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200

  def on_delete(self, req, res,table):
    self.api['method'] = 'DELELTE'
    self.api['table'] = table
    self.api['deleted'] = False
    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)

    if self.api['exists']: 
      client.delete_table(table)
      self.api['deleted'] = True


    res.body = json.dumps(self.api)
    res.status = falcon.HTTP_200

