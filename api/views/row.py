#!/usr/bin/env python
import time
import falcon
import json
import kudu
import uuid
from kudu.client import Partitioning
from datetime import datetime

class Row:

  def __init__(self,config):
   self.config = config

  def on_get(self, req, res,table,row):
    api = {
     'table'   : table,
     'row'     : row,
     'errors'  : []
     }
    client = kudu.connect(host='queen', port=7051)
    if client.table_exists(table):
      if row.isdigit():
        row_id  = int(row)
        table   = client.table(table)
        scanner = table.scanner()
        #api['scanner'] = dir(scanner)
        scanner.add_predicate(table['_id'] == row_id )
        ret = scanner.open().read_all_tuples()
        api['ret'] =ret
      else:
        api['errors'].append('Row is not an integer/number')
    else:
      api['errors'].append('Table does not exist')
    res.body = json.dumps(api)
    res.status = falcon.HTTP_200



  def on_put(self, req, res,table,row):
    api = {
     'table'  : table,
     'success': False,
     'errors' : [] 
     }
    client = kudu.connect(host='queen', port=7051)
    session = client.new_session()
    if client.table_exists(table): 
      tb = client.table(table)
      sm = tb.schema
      data   = json.load(req.bounded_stream)
      table   = client.table(table)
      schema = {}      
      for i in sm:
        schema[i.name] = i.type.name


      scanner = table.scanner()
      #scanner.set_limit(1) #no supported with 1.2
      api['scanner'] = dir(scanner)
      #scanner.add_predicate(table['_id'] == row_id )
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')
      print(schema)
      print('xxxxxxxxxxxxxxxxxxxxxxxxxxx')



      """
      if row.isdigit():
        api['update'] = True
      else:
        #adpi['dir-table'] = dir(table)
        op = table.new_insert()
        op['_id'] = uuid.uuid4().int>>1
 
        op['style'] = 'xxxx'
        op['qty'] = 1
        op['cost'] = 1
        op['price'] = 1
        op['hash'] = 'xxxxx'
        session.apply(op)
        session.flush()
        api['success'] = True
        api['insert'] = True
       """
    else:
      api['errors'].append('Table does not exist')

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200

