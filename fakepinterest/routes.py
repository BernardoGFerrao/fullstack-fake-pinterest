#Onde vamos criar as rotas do site/links
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta
from fakepinterest.models import Usuario, Post

@app.route('/', methods=['GET', 'POST'])
#Criando uma rota(Caminho para o link do site)( / -> Homepage)
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():#Se o usuário preencheu o login e está válido:
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data):#Se existe um usuário com esse email e a senha digitada no formulario coincide com a do db
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():#Se o usuário clicar no botão e as informações estiverem preenchidas:
        #Criar um objeto do tipo Usuário:
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data)#Criptografa a senha do usuário
        usuario = Usuario(username=formcriarconta.username.data,
                          email=formcriarconta.email.data,
                          senha=senha)
        #Enviar o Usuário para o db:
        database.session.add(usuario)
        database.session.commit()
        #Fazer o login do usuário:
        login_user(usuario, remember=True)
        #Redirecionar o usuário:
        return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('criarconta.html', form=formcriarconta)


#Para não precisar criar uma rota para cada pessoa -> Páginas dinâmicas
@app.route(f'/perfil/<id_usuario>')
@login_required
def perfil(id_usuario):
    if id_usuario == current_user.id:
        #O usuário está no seu perfil
        return render_template('perfil.html', usuario=current_user)#render template permite conversar com o html
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario)#render template permite conversar com o html

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))