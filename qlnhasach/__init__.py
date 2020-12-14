from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "Fw\xc6\xab\x1bM\x82\xe1$\xf08\x91js\x92\x9d"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Phuong123%@localhost/qlnhasachdb?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app,
              name='Quản lí nhà sách',

              template_mode='bootstrap4')

login_manager = LoginManager(app)

