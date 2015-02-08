from datetime import datetime

class Ruling(object):
  def __init__(self, source, alternate, author, date_of_ruling, content, added_by):
    self.source = source
    self.alternate = alternate
    self.author = author
    self.date_of_ruling = date_of_ruling
    self.content = content
    self.added_by = added_by
    self.invalidates = []
    self.references = []
    self.time = datetime.utcnow()
    self.id = hex(hash(tuple([source, author, date_of_ruling, added_by, self.time])))[2:]
    
  def __repr__(self):
    return '<%s %r>' % (type(self).__name__, self.source)
