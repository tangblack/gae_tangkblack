import cgi
from model.store import Store
from model.store import Product
from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app


STORE_KEY = 'singleton_store'
ADMIN_MAIL = u'tangblack@gmail.com'


def get_store():
    store = memcache.get(STORE_KEY)
    if store is None:
        store = Store.get_by_key_name(STORE_KEY)
        memcache.set(STORE_KEY, store)
    return store
    

class StorePage(webapp.RequestHandler):
    def get(self):
        store = get_store()
        products = None
        if store:
            products = store.products
        content = template.render('./template/store/store.html', 
                                  {'store' : store,
                                   'products' : products})
        self.response.out.write(content)
        
        
class ProductPage(webapp.RequestHandler):
    def get(self, key):
        store = get_store()
        product = db.get(key)
        content = template.render('./template/store/product.html', 
                                  {'store' : store,
                                   'product' : product})
        self.response.out.write(content)
    def post(self):
        self.response.out.write('na')
        

class AdminProductPage(webapp.RequestHandler):
    def get(self):
        store = get_store()
        action = self.request.get('action', default_value='unknown')
        if action == 'create':
            content = template.render('./template/store/edit_product.html', 
                                  {'store' : store})
            self.response.out.write(content)
        elif action == 'update':
            key = self.request.get('key')
            product = db.get(key)
            content = template.render('./template/store/edit_product.html', 
                                  {'store' : store,
                                   'product' : product})
            self.response.out.write(content)
        elif action == 'delete':
            key = self.request.get('key')
            db.delete(key)
            self.redirect('/store/admin')
        else:
            self.response.out.write('na')
    def post(self):
        action = self.request.get('action', default_value='unknown')
        if action == 'save':
            key = self.request.get('key')
            # create
            if key is None or len(key) <= 0:
                product = Product(name = self.request.get('name'), 
                                  price = int(self.request.get('price')),
                                  content = self.request.get('content'),
                                  hide = bool(int(self.request.get('hide'))),
                                  store = get_store())
            else:
                # update
                product = db.get(key)
                product.name = self.request.get('name')
                product.price = int(self.request.get('price'))
                product.content = self.request.get('content')
                product.hide = bool(int(self.request.get('hide')))
            product.put()
        else:
            self.response.out.write('na')
        self.redirect('/store/admin')


class AdminInitStorePage(webapp.RequestHandler):
    def get(self):
        store = get_store()
        if store is None:
            store = Store(key_name=STORE_KEY,
                                name='My Store',
                                description='This is my store')
            store.put()
            memcache.delete(STORE_KEY)
            memcache.set(STORE_KEY, store)
        self.redirect('/store')


class AdminEditStorePage(webapp.RequestHandler):
    def get(self):
        store = get_store()
        if store is None:
            self.response.out.write('Store Not Found')
        else:
            content = template.render('./template/store/edit_store.html', 
                                      {'store' : store})
            self.response.out.write(content)
            
    def post(self):
        name = self.request.get('name')
        description = self.request.get('description')
        self.response.out.write(name)
        
        store = get_store()
        if store is None:
            self.response.out.write('Store Not Found')
        else:
            store.name = name
            store.description = description
            store.put()
            memcache.delete(STORE_KEY)
            memcache.set(STORE_KEY, store)
            self.redirect('/store/admin')
        
                
class AdminPage(webapp.RequestHandler):
    def get(self):
        store = get_store()
        products = None
        if store:
            products = store.products
        content = template.render('./template/store/admin.html', 
                                  {'store' : store,
                                   'products' : products})
        self.response.out.write(content)
        
        
class ProductBuyPage(webapp.RequestHandler):
    def get(self, key):
        store = get_store()
        product = db.get(key)
        content = template.render('./template/store/buy.html', 
                                  {'store' : store,
                                   'product' : product})
        self.response.out.write(content)
    def post(self, key):
        product = db.get(key)
        name = cgi.escape(self.request.get('name'))
        e_mail = cgi.escape(self.request.get('mail'))
        phone = cgi.escape(self.request.get('phone'))
        address = cgi.escape(self.request.get('address'))
        comment = cgi.escape(self.request.get('comment'))
        user = users.get_current_user()
        body = u"" + "name:" + name + "\n" + "mail:" + e_mail + "\n" + "phone:" + phone + "\n" + "address:" + address + "\n" + "comment:" + comment + "\n"
        # send mail
        mail.send_mail(user.email(), ADMIN_MAIL, product.name, body)
        store = get_store()
        content = template.render('./template/store/product.html', 
                                  {'store' : store,
                                   'product' : product})
        self.response.out.write(content)
        
        
application = webapp.WSGIApplication([('/store', StorePage),
                                       ('/store/product/(.*)/buy', ProductBuyPage),
                                       ('/store/product/(.*)', ProductPage),
                                       ('/store/admin/product', AdminProductPage),
                                       ('/store/admin/init_store', AdminInitStorePage),
                                       ('/store/admin/edit_store', AdminEditStorePage),
                                       ('/store/admin', AdminPage)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()