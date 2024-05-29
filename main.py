from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
#Criando uma rota(Caminho para o link do site)( / -> Homepage)
def homepage():
    return render_template('homepage.html')

#Para não precisar criar uma rota para cada pessoa -> Páginas dinâmicas
@app.route(f'/perfil/<usuario>')
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)#render template permite conversar com o html

if __name__ == '__main__':
    app.run(debug=True)