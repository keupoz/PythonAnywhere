from utils import timer

def serverRegisterer (servers):
  def wrapper (name):
    def register (func):
      servers[name] = func
      return func
    return register
  return wrapper

def skinCache (cacheObject):
  def wrapper (getSkin):
    def execute (uuid):
      skin = cacheObject.get(uuid)
      if skin: return skin
      
      skin = getSkin(uuid)
      cacheObject[uuid] = skin
      
      @timer(60)
      def delCache ():
        del cacheObject[uuid]
      
      return skin
    return execute
  return wrapper
