from requests import get

from ponyskins import decorators, Yggdrasil

MOJANG_ID   = 'https://api.mojang.com/users/profiles/minecraft/%s'
MOJANG_TX   = 'https://sessionserver.mojang.com/session/minecraft/profile/%s'
VALHALLA_TX = 'http://skins.minelittlepony-mod.com/user/%s'
LEGACY_SKIN = 'http://skins.voxelmodpack.com/skins/%s.png'

SERVERS = dict()
server = decorators.serverRegisterer(SERVERS)

def getMojangProfile (nickname):
  r = get(MOJANG_ID % nickname)
  return None if r.status_code == 204 else r.json()

@server('valhalla')
def getSkinValhalla (uuid):
  r = get(VALHALLA_TX % uuid)

  if r.status_code != 200:
    return None

  return Yggdrasil.texture(r.json()['textures'], 'SKIN')

@server('legacy')
def getSkinLegacy (uuid):
  r = get(LEGACY_SKIN % uuid)

  if r.status_code == 404: return None
  else: return { 'skin': r.content, 'model': None }

@server('mojang')
@decorators.skinCache(dict())
def getSkinMojang (uuid):
  txs = Yggdrasil.textures(MOJANG_TX, uuid)

  if not txs:
    return None

  return Yggdrasil.texture(txs['textures'], 'SKIN')


def getSkin (server, uuid, recursive):
  if recursive:
    servers = list(SERVERS.keys())
    i = servers.index(server)
    skin = None

    while (skin is None) and (i < len(servers)):
      skin = SERVERS[servers[i]](uuid)
      i += 1

    return skin

  else:
    return SERVERS[server](uuid)
