from flask import request

from utils import err, cors_response
from ponyskins import getters


def no_server ():
  return err('No server provided')

def no_nickname (**opts):
  return err('No nickname provided')

def process_nickname (server, nickname):
  if not getters.SERVERS.get(server):
    return err('Unknown server')

  profile = getters.getMojangProfile(nickname)

  if not profile:
    return err('No profile for nickname "%s"' % nickname, 404)

  result = getters.getSkin(server, profile['id'], request.args.get('recursive') == '')

  if not result:
    return err('No skin for nickname "%s"' % profile['name'], 404)

  return cors_response(result['skin'], 200,
    { 'Content-Type': 'image/png' },
    {
      'X-Nickname': profile['name'],
      'X-Model': result['model']
    })


def init (route, app, rootpath):
  route('/', no_server)
  route('/<server>/', no_nickname)
  route('/<server>/<nickname>', process_nickname)
