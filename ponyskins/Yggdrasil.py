from requests import get

from base64 import b64decode
import json

def profile (url, nickname):
  r = get(url % nickname)
  return None if r.status_code == 204 else r.json()

def textures (url, uuid):
  r = get(url % uuid)
  
  if r.status_code != 200:
    return None
  
  return json.loads(b64decode(r.json()['properties'][0]['value']))

def texture (textures, tex_type):
  tx = textures.get(tex_type)
  
  if not tx:
    return None
  
  metadata = tx.get('metadata')
  model = metadata.get('model') if metadata else None
  
  r = get(tx['url'])
  
  if r.status_code == 404:
    return None
  
  else: return { 'skin': r.content, 'model': model }
