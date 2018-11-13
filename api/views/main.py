#!/usr/bin/env python
import time
import falcon
import json

class Main:

  def __init__(self,config):
   self.config = config

  def on_get(self, req, res):
      res.content_type = 'falcon.MEDIA_HTML'
      res.body  = """
      <!DOCTYPE html>
      <html>
      <head>
      <title>KUDU API</title>
      </head>
      <body>
      <h1>KUDU API</h1>
      </body>
      </html>
      """
      
      res.status = falcon.HTTP_200
 
