from flask import Flask

app = Flask(__name__)

@app.route('/')
#Criando uma rota(Caminho para o link do site)( / -> Homepage)
def homepage():
    return 'Fake Pinterest - Home page'

if __name__ == '__main__':
    app.run(debug=True)