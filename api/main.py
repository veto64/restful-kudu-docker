#!env python
import falcon
import yaml
from api.views import main,sal_api
from falcon_cors import CORS


def get_app():

  cors = CORS(allow_all_origins=True)
  api = falcon.API(middleware=[cors.middleware])

  routes = []

  with open("config.yml", 'r') as stream:
    try:
      config = yaml.safe_load(stream)

      routes.append(('/customers', customers.Customers(config)))
      routes.append(('/main', main.Main(config)))
      routes.append(('/', sal_api.Sal_api(config, routes)))  # has to be the last one
      
    except yaml.YAMLError as exc:
      config = False

  if config:
    for route in routes:
      api.add_route(*route)

  return api


