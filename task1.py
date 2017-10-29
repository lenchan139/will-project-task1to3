
import webapp2
from datetime import datetime
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<br/><a href='/'>Back</a><br/>")
        strCurrentTime = "<h2>The current time is: </h2>"
        time = "<h3>" + str(datetime.now()) + "</h3>"
        strRefreshButton = "<h4><b><a href='.'>Refresh</a></b></h4>"
        self.response.write(strCurrentTime + time + strRefreshButton)

app = webapp2.WSGIApplication([
    ('/task1/', MainHandler)
], debug=True)
