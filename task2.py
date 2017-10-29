
import webapp2
from google.appengine.api import users
from google.appengine.api import memcache
from webapp2_extras import sessions

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
        user = users.get_current_user()
        self.response.write("<br/><a href='/'>Back</a><br/>")
        self.response.write('<h3>Save display name uses session.</h3>')
        name = self.session.get('name')
        if user:
            logout_url = users.create_logout_url('/task2/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
            name, logout_url)
        else:
            login_url = users.create_login_url('/task2/signin/')
            greeting = '<a href="/task2/signin/">Sign in</a>'

        self.response.write(greeting)





class SignHandler(BaseHandler):

    def get(self):
            strForm  = "<h3>Enter your nickname before login</h3>"
            strForm += "<form method='post'>"
            strForm += "Nickname: "
            strForm += "<input type='text' name='name'/>"
            strForm += "<input type='submit' /><br/>"
            strForm += "</form>"
            self.response.write(strForm)

    def post(self):
        user = users.get_current_user()
        name = self.request.get('name')
        if self.request.get('name'):
            self.session['name'] = name

        if user:
            self.redirect('/task2/')
        else:
            login_url = users.create_login_url('/task2/')
            self.redirect(login_url)




config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'testkey11111',
}
app = webapp2.WSGIApplication([
    ('/task2/', MainHandler),
    ('/task2/signin/', SignHandler),
], config=config, debug=True)
