import base64, operator, os

import cherrypy
from genshi.template import TemplateLoader
from tmm.model import Ruling
from libs import template

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
        
  @cherrypy.expose
  @template.output('ruling.html')
  def ruling(self, a):
    r = self.data[base64.b64decode(a)]
    return template.render(ruling=r)
