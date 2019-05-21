from flask import make_response

from threading import Timer
import json


def cors_response (content, code=200, cheaders=None, xheaders=None):
  if type(content) is dict:
    return json_response(content, code)
  
  if type(content) is str:
    content = content.encode('utf-8')
  
  response = make_response(content)
  response.status_code = code
  
  if cheaders: response.headers.extend(cheaders)
  
  response.headers.set('Access-Control-Allow-Origin', '*')
  
  if xheaders: 
    response.headers.set('Access-Control-Expose-Headers', ','.join(xheaders.keys()))
    response.headers.extend(xheaders)
  
  return response


def json_response (obj, code=200):
  if type(obj) is not dict:
    return cors_response(obj, code)
  
  content  = json.dumps(obj)
  response = cors_response(content, code)
  response.headers.set('Content-Type', 'application/json')
  
  return response

def err (msg, code=400):
  return json_response({ 'error': msg }, code)


def timer (seconds):
  def wrapper (func):
    Timer(seconds, func).start()
  return wrapper
