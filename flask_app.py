from flask import Flask

from ponyskins import PonySkins

app = Flask(__name__)

def init_module (module, rootpath):
  def route (subpath, view_fn, **options):
    app.add_url_rule(rootpath + subpath, view_func=view_fn, **options)
  
  module.init(route, app, rootpath)


init_module(PonySkins, '/ponyskins')
