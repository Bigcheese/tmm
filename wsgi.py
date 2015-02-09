import os, pickle, sys
import cherrypy
from tmm.controller import Root

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
  cherrypy.config.update({'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__))})
  cherrypy.quickstart(Root(data), '/', 'tmm.conf')
  
if __name__ == '__main__':
  main(sys.argv[1])
