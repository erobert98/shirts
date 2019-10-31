from flask import Flask
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_sslify import SSLify
from flask_login import LoginManager
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
from flask_security import Security, SQLAlchemyUserDatastore
# import shopify
import os


app = Flask(__name__)
Bootstrap(app)
# sslify = SSLify(app)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
# shop_url = "https://88a56f54b8b8afe3ed9159d650ab650c:0a9ace65d62c275bb3772607af64e103@dub-denim-shirts.myshopify.com/admin/api/2019-10"
# shopify.ShopifyResource.set_site(shop_url)

migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models
from app.models import User, Role

# admin = Admin(app, name='laneck', template_mode='bootstrap3')
# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Role, db.session))
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)