#!/usr/bin/env python
import time
import kudu
from kudu.client import Partitioning
from datetime import datetime

table_name = 'master_foo'
# Mount/connect the Kudu queen 
client = kudu.connect(host='queen', port=7051)


builder = kudu.schema_builder()
builder.add_column('key').type(kudu.int64).nullable(False).primary_key()
builder.add_column('name').type(kudu.string)
schema = builder.build()
partitioning = Partitioning().add_hash_partitions(column_names=['key'], num_buckets=3)


try: 
  print('...try to open the table')
  table = client.table(table_name)
except Exception as e:
  print('...create table')
  client.create_table(table_name, schema, partitioning)  
  print('...wait 3 sec before access the table')
  time.sleep(3)
  table = client.table(table_name)
  no = 10000
  for i in range(no):
    print('add row {}'.format(no-i))
    op = table.new_insert({'key': i, 'name': 'foo{}'.format(i)})
    session = client.new_session()
    session.apply(op)
    session.flush()
    
scanner = table.scanner()
ret = scanner.open().read_all_tuples()
for i in ret:
  print('key: {} name: {}'.format(i[0],i[1]))

