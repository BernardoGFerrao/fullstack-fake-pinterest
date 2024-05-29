#Criar o banco de dados:
from fakepinterest import database, app
from fakepinterest.models import Usuario, Post

#Cria um banco SQL
with app.app_context():
    database.create_all()
