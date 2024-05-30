#Onde vamos criar as rotas do site/links
from flask import render_template, url_for
from fakepinterest import app
from flask_login import login_required
from fakepinterest.forms import FormLogin, FormCriarConta

@app.route('/', methods=['GET', 'POST'])
#Criando uma rota(Caminho para o link do site)( / -> Homepage)
def homepage():
    formlogin = FormLogin()
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    return render_template('criarconta.html', form=formcriarconta)


#Para não precisar criar uma rota para cada pessoa -> Páginas dinâmicas
@app.route(f'/perfil/<usuario>')
@login_required
def perfil(usuario):
    return render_template('perfil.html', usuario=usuario)#render template permite conversar com o html

