from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#Passar o local onde db se localiza
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SECRET_KEY'] = '2dec8a3200646a30ce0dc5a741c47925'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)#Criptografia
login_manager = LoginManager(app)
login_manager.login_view = "homepage" #Rota que gerencia o login


#Importação
from fakepinterest import routes