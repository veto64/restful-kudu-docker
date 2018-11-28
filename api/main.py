#!env python
import falcon
import yaml
from views import main,table,tables
from falcon_cors import CORS


cors = CORS(allow_all_origins=True)
api = falcon.API(middleware=[cors.middleware])

with open("config.yml", 'r') as stream:
  try:
    config = yaml.safe_load(stream)
  except yaml.YAMLError as exc:
    config = False

if config:
  api.add_route('/', tables.Tables(config))
  api.add_route('/tables', tables.Tables(config))
  api.add_route('/{table}', table.Table(config))



