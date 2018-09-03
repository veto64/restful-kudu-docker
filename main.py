#!/usr/bin/env python
import kudu
from kudu.client import Partitioning
from datetime import datetime

# Connect to Kudu master server
client = kudu.connect(host='127.0.0.1', port=7051)


builder = kudu.schema_builder()
builder.add_column('key').type(kudu.int64).nullable(False).primary_key()
builder.add_column('ts_val', type_=kudu.unixtime_micros, nullable=False, compression='lz4')
schema = builder.build()

partitioning = Partitioning().add_hash_partitions(column_names=['key'], num_buckets=3)
client.create_table('foo', schema, partitioning)

"""
table = client.table('python-example')
session = client.new_session()
op = table.new_insert({'key': 1, 'ts_val': datetime.utcnow()})
session.apply(op)
op = table.new_upsert({'key': 2, 'ts_val': "2016-01-01T00:00:00.000000"})
session.apply(op)
op = table.new_update({'key': 1, 'ts_val': ("2017-01-01", "%Y-%m-%d")})
session.apply(op)
op = table.new_delete({'key': 2})
session.apply(op)
try:
    session.flush()
except kudu.KuduBadStatus as e:
    print(session.get_pending_errors())
scanner = table.scanner()
scanner.add_predicate(table['ts_val'] == datetime(2017, 1, 1))
result = scanner.open().read_all_tuples()
"""
