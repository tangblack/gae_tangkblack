from google.appengine.ext import db

class Store(db.Model):
    name = db.StringProperty(required=True)
    description = db.StringProperty(required=True, default='')
    

class Product(db.Model):
    store = db.ReferenceProperty(reference_class=Store, collection_name='products')
    name = db.StringProperty(required=True)
    price = db.IntegerProperty(required=True, default=0)
    content = db.TextProperty(required=True, default=db.Text('')) 
    hide = db.BooleanProperty(required=True, default=False)