import os
import urllib
import ast
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions
from random import randint

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()


class MainHandler(BaseHandler):
    def get(self):
        self.session['number'] = randint(0, 99)
        number = self.session.get('number')
        template_values = {
            'number': number,
        }
        template = JINJA_ENVIRONMENT.get_template('task3temp.html')
        self.response.write(template.render(template_values))

    def post(self):
        number = int(self.session.get('number'))
        if self.request.get('userNum') :
            userNum = int(self.request.get('userNum'))
        else:
            self.redirect('/task3/')
        # 3 -  3 =  0
        # 3 - 15 = -x
        # 15 - 3 = +x
        if (userNum - number) == 0 :
            msgCompare = "similar"
        elif (userNum - number) < 0:
            msgCompare = "Too small"
        elif (userNum - number) > 0:
            msgCompare = "Too big"
        else:
            self.redirect('/task3/')

        template_values = {
            'number': number,
            'userNum': userNum,
            'msgCompare': msgCompare,
        }
        template = JINJA_ENVIRONMENT.get_template('task3temp.html')
        self.response.write(template.render(template_values))
        # self.response.write("")

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'testkey11111',
}
app = webapp2.WSGIApplication([
    ('/task3/', MainHandler)
],config=config, debug=True)
