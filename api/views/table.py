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

    self.api['data']   = json.load(req.bounded_stream)

    client = kudu.connect(host='queen', port=7051)
    self.api['exists'] = client.table_exists(table)

    if not self.api['exists']: 
      builder = kudu.schema_builder()
      builder.add_column('id').type(kudu.int64).nullable(False).primary_key()
      if self.api['data']:
        for i in self.api['data']:
          if self.api['data'][i] == 'int':
            builder.add_column(i).type(kudu.int64)
          elif self.api['data'][i] == 'time':
            builder.add_column(i).type(kudu.unixtime_micros)
          elif self.api['data'][i] == 'float':
            builder.add_column(i).type(kudu.float)
          elif self.api['data'][i] == 'double':
            builder.add_column(i).type(kudu.float)
          elif self.api['data'][i] == 'decimal':
            builder.add_column(i).type(kudu.decimal)
          elif self.api['data'][i] == 'binary':
            builder.add_column(i).type(kudu.binary)
          elif self.api['data'][i] == 'bool':
            builder.add_column(i).type(kudu.binary)
          else:
            builder.add_column(i).type(kudu.bool)
      schema = builder.build()
      partitioning = Partitioning().add_hash_partitions(column_names=['id'], num_buckets=3) 
      client.create_table(table, schema, partitioning)  
      self.api['created'] = True

    res.body = json.dumps(self.api)
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

