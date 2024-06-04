from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Usuarios
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        alias = request.form.get('alias')
        contrasena = request.form.get('contrasena')

        user_verified = Usuarios.query.filter_by(alias=alias).first()
        if user_verified:
            if check_password_hash(user_verified.contrasena, contrasena):
                flash('Logged in successfully!', category='success')
                login_user(user_verified, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
                print('aaafsaa')
        else:
            flash('user does not exist.', category='error')
            print('aaa')

    return render_template("login.html")


@auth.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        alias = request.form.get('alias')
        nombre = request.form.get('name')
        apellidos = request.form.get('surname')
        telefono = request.form.get('tel')
        email = request.form.get('email')
        contrasena = request.form.get('pswd1')
        contrasena2 = request.form.get('pswd2')
        id_tipo = 1
        alta = True
        fecha_creacion = datetime.today().strftime('%Y-%m-%d')
        comentario = "Nuevo usuario"

        user = Usuarios.query.filter_by(alias=alias).first()

        if user:
            flash('Este nombre de usuario ya existe', category='error')
        elif len(nombre) < 2:
            flash('El nombre debe de tener mas de 2 caracteres', category='error')
        elif len(apellidos) < 2:
            flash('El apellido debe de tener mas de 2 caracteres', category='error')
        elif contrasena != contrasena2:
            flash('Las contraseñas no coinciden', category='error')
        elif len(contrasena) < 3:
            flash('La contraseña debe de ser de 3 caracteres como mínimo', category='error')
        else:
            new_user = Usuarios(
                alias=alias,
                nombre=nombre,
                apellidos=apellidos,
                telefono=telefono,
                email=email,
                fecha_creacion=fecha_creacion,
                comentario=comentario,
                id_tipo=id_tipo,
                alta=alta,
                contrasena=generate_password_hash(contrasena, method='pbkdf2:sha256'),
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            useralias = new_user.alias
            return redirect(url_for('views.home'))

    return render_template('signup.html')





@auth.route('/user',methods=['GET', 'POST'])
def user():
    return render_template('usuario.html')