import operator, os, pickle, sys
import cherrypy
from genshi.template import TemplateLoader
from tmm.model import Ruling
from tmm.lib import template

loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'templates'),
    auto_reload = True)

class Root(object):
  def __init__(self, data):
    self.data = data
    
  @cherrypy.expose
  @template.output('index.html')
  def index(self):
    rulings = sorted(self.data.values(), key = operator.attrgetter('time'))
    return template.render(rulings=rulings)
    
  @cherrypy.expose
  @template.output('submit.html')
  def submit(self, cancel=False, **data):
    if cherrypy.request.method == 'POST':
      if cancel:
        raise cherrypy.HTTPRedirect('/')
      ruling = Ruling(**data)
      self.data[ruling.id] = ruling
      raise cherrypy.HTTPRedirect('/')
    
    return template.render()

def main(filename):
  if os.path.exists(filename):
    fileobj = open(filename, 'rb')
    try:
      data = pickle.load(fileobj)
    finally:
      fileobj.close()
  else:
    data = {}
    
  def _save_data():
    fileobj = open(filename, 'wb')
    try:
      pickle.dump(data, fileobj)
    finally:
      fileobj.close()
  
  cherrypy.engine.subscribe('stop', _save_data)
  
  cherrypy.config.update({
      'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
      'tools.decode.on': True,
      'tools.trailing_slash.on': True,
      'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
  })
  
  cherrypy.quickstart(Root(data), '/', {
    '/media': {
      'tools.staticdir.on': True,
      'tools.staticdir.dir': 'static'
    }
  })
  
if __name__ == '__main__':
  main(sys.argv[1])
