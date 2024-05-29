from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Passar o local onde db se localiza
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

database = SQLAlchemy(app)

#Importação
from fakepinterest import routes