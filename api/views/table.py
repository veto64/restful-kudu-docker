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

  def on_get(self, req, res,table):
    api = {
     'table' : table
     }
    client = kudu.connect(host='queen', port=7051)
    if client.table_exists(table):
      api['success'] = 'Table ok'
    else:
      api['errors'].append('Table does not exist')

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200



  def on_put(self, req, res,table):
    api = {
     'table': table,
     'success': False
     }
    data   = json.load(req.bounded_stream)
    client = kudu.connect(host='queen', port=7051)
    if not client.table_exists(table): 
      builder = kudu.schema_builder()
      builder.add_column('id').type(kudu.int64).nullable(False).primary_key()

      if data:
        for i in data:
          if data[i] == 'string':
            builder.add_column(i).type(kudu.string)
          elif data[i] == 'int':
            builder.add_column(i).type(kudu.int64)
          elif data[i] == 'time':
            builder.add_column(i).type(kudu.unixtime_micros)
          elif data[i] == 'float':
            builder.add_column(i).type(kudu.float)
          elif data[i] == 'double':
            builder.add_column(i).type(kudu.float)
          elif data[i] == 'decimal':
            builder.add_column(i).type(kudu.decimal)
          elif data[i] == 'binary':
            builder.add_column(i).type(kudu.binary)
          elif data[i] == 'bool':
            builder.add_column(i).type(kudu.bool)
          else:
            builder.add_column(i).type(kudu.string)

      schema = builder.build()
      partitioning = Partitioning().add_hash_partitions(column_names=['id'], num_buckets=3) 
      client.create_table(table, schema, partitioning)  
      api['success'] = True

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200

  def on_update(self, req, res,table):
    self.api['method']  = 'UPDATE'
    self.api['table']   = table
    self.api['exists']  = False
    self.api['update']  = []
    self.api['error']   = []

    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)
    if self.api['exists']:
      self.api['rename'] = req.get_param('name')
      self.api['data']   = json.load(req.bounded_stream)
      otable = client.table(table)
      alt = client.new_table_alterer(otable)
      if self.api['data']:
        if 'cols' in self.api['data']:
          for i in self.api['data']['cols']:
            try:
              alt.alter_column(i,self.api['data']['cols'][i])
              alt.alter()
              self.api['update'].append([i,self.api['data']['cols'][i]])
            except Exception as e:
              self.api['error'].append(str(e))

      if self.api['rename']:
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
    api = {
     'success': False
     }
    client = kudu.connect(host='queen', port=7051)

    if client.table_exists(table):
      client.delete_table(table)
      api['success'] = True
    else:
      api['error'] = ['Table does not exist']

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200

