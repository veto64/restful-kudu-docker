#!/usr/bin/env python
import time
import falcon
import json
import jwt
from api.views import main,tokens

class Main:

  def __init__(self,config):
   self.config = config

  def on_get(self, req, res):
    """Handles GET requests"""
    e = jwt.encode(
      {'some': 'payload','exp': int(time.time()-100)},
      'secret',
      algorithm='HS256')

    try:
      d = jwt.decode(e, 'secret', algorithms=['HS256'])
      print(d,int(time.time()))
      data = {'code': 'hello'}
      res.body = json.dumps(data)
      res.status = falcon.HTTP_200
    except jwt.ExpiredSignatureError:
      res.content_type = 'falcon.MEDIA_HTML'
      data = {'msg': 'token expired'}    
      res.body  = """
      <!DOCTYPE html>
      <html>
      <head>
      <title>Request Token</title>
      </head>
      <body>
      <h1>Your Token expired, please request another.</h1>
      <p>Request Token:</p>
      <form method="get" action="/tokens">
       <fieldset>
         <label>Username:<br/><input name="name" /></label><br/>
         <label>Password:<br/><input name="password" /></label><br/>
         <input type="submit" value="Get" />
       </fieldset>
      </form>
      <br/>
      <a href="http://wiki.salamander-jewelry.net/index.php/API3">Wiki</a>
      </body>
      </html>
      """
      
      res.status = falcon.HTTP_200
 
