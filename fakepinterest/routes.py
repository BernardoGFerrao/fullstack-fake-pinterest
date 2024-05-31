#Onde vamos criar as rotas do site/links
from flask import render_template, url_for, redirect
from fakepinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepinterest.forms import FormLogin, FormCriarConta, FormFoto
from fakepinterest.models import Usuario, Post
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
#Criando uma rota(Caminho para o link do site)( / -> Homepage)
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():#Se o usuário preencheu o login e está válido:
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), formlogin.senha.data):#Se existe um usuário com esse email e a senha digitada no formulario coincide com a do db
            login_user(usuario)
            return redirect(url_for('perfil', id_usuario=usuario.id))
    return render_template('homepage.html', form=formlogin)

@app.route('/criarconta', methods=['GET', 'POST'])
def criarconta():
    formcriarconta = FormCriarConta()
    if formcriarconta.validate_on_submit():#Se o usuário clicar no botão e as informações estiverem preenchidas:
        #Criar um objeto do tipo Usuário:
        senha = bcrypt.generate_password_hash(formcriarconta.senha.data).decode("utf-8")#Criptografa a senha do usuário
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
@app.route(f'/perfil/<id_usuario>', methods=['GET', 'POST'])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        #O usuário está no seu perfil
        #Postar fotos
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            #Filtro de nomes
            nome_seguro = secure_filename(arquivo.filename)
            #Salvar o arquivo na pasta fotos_post
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho)
            #Registrar no db
            post = Post(imagem=nome_seguro, id_usuario=current_user.id)
            database.session.add(post)
            database.session.commit()
        return render_template('perfil.html', usuario=current_user, form=form_foto)#render template permite conversar com o html
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html', usuario=usuario, form=None)#render template permite conversar com o html

@app.route('/feed')
@login_required
def feed():
    fotos = Post.query.order_by(Post.data_criacao.desc()).all()
    return render_template('feed.html', fotos=fotos)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))
