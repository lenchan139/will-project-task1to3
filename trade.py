
import webapp2
from datetime import datetime
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h1>NO TRADE WITH PY, IT IS SO HORRIBLE!!!</h1>")

app = webapp2.WSGIApplication([
    ('/pytrade/', MainHandler)
], debug=True)
