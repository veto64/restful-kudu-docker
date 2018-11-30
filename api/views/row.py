#!/usr/bin/env python
import time
import falcon
import json
import kudu
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
        scanner.add_predicate(table['id'] == row_id )
        ret = scanner.open().read_all_tuples()
        api['ret'] =ret
      else:
        api['errors'].append('Row is not an integer/number')
    else:
      api['errors'].append('Table does not exist')
    res.body = json.dumps(api)
    res.status = falcon.HTTP_200



  def on_put(self, req, res,table,row):
    data   = json.load(req.bounded_stream)
    api = {
     'table'  : table,
     'success': False,
     'errors' : [] 
     }
    client = kudu.connect(host='queen', port=7051)
    session = client.new_session()
    if client.table_exists(table): 
      table   = client.table(table)
      if row.isdigit():
        api['update'] = True
      else:
        #adpi['dir-table'] = dir(table)
        op = table.new_insert()
        op['id'] = 2
        op['style'] = 'xxxx'
        op['qty'] = 1
        op['cost'] = 1
        op['price'] = 1
        op['hash'] = 'xxxxx'

        #for k,v in data.items():
        #  op[k]= v
        session.apply(op)
        #api['op'] = str(dir(op))
        session.flush()
        api['insert'] = True
                        
    else:
      api['errors'].append('Table does not exist')

    res.body = json.dumps(api)
    res.status = falcon.HTTP_200

