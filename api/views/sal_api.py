import json
import falcon


class Sal_api:
  def __init__(self, conf, routes):
    self.conf = conf
    self.route_descriptions = {}

    for route in routes:
      method_list = list(falcon.routing.map_http_methods(route[1]).keys())
      # falcon.routing.compile_uri_template(route[0]) #extract uri params
      self.route_descriptions[route[0]] = {'METHODS': method_list}

  def on_get(self, req, resp):
      resp.body = json.dumps(self.route_descriptions, ensure_ascii=False)
      resp.status = falcon.HTTP_200
