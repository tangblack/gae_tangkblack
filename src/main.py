import positional_notation
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class MainPage(webapp.RequestHandler):
    def get(self):
        self.redirect('http://tangblack.blogspot.com/')
#        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write('Hello, webapp World!')


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/positional_notation', positional_notation.PositionalNotationPage)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
