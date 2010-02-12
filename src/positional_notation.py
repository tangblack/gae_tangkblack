import util
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class PositionalNotationPage(webapp.RequestHandler):
    def get(self):
        content = template.render('./template/positional_notation/positional_notation.html', {})
        self.response.out.write(content)
        
    def post(self):
        value = 0
        try:
            # Get input value from user.
            # Translate to decimal value.
            if len(self.request.get('binary')) > 0:
                value_str = self.request.get('binary')
                value = int(value_str, 2)
            elif len(self.request.get('octal')) > 0:
                value_str = self.request.get('octal')
                value = int(value_str, 8)
            elif len(self.request.get('decimal')) > 0:
                value_str = self.request.get('decimal')
                value = int(value_str, 10)
            elif len(self.request.get('hexadecimal')) > 0:
                value_str = self.request.get('hexadecimal')
                value = int(value_str, 16)
            else:
                self.redirect('/positional_notation')
                
            # Get result. 
            binary = util.denary_to_binary(value)
            octal = oct(value)
            decimal = value
            hexadecimal = hex(value)
            content = template.render('./template/positional_notation/positional_notation_result.html', 
                                                {'binary' : binary,
                                                 'octal' : octal,
                                                 'decimal' : decimal,
                                                 'hexadecimal' : hexadecimal})
            self.response.out.write(content)
        except:
            self.redirect('/positional_notation')
            
    
application = webapp.WSGIApplication([('/positional_notation', PositionalNotationPage)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()