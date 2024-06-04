from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from . import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///juegarapido.db'

# Define database models
class CategoriasJuegos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    comentario = db.Column(db.Text)

class CategoriasRecords(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    comentario = db.Column(db.Text)

class Juegos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.Text)
    fecha = db.Column(db.DateTime)
    imagen = db.Column(db.Text)
    categoria_id = db.Column(db.Integer)
    archivos = db.relationship('Archivos', backref='juego', lazy='dynamic')
    resennas = db.relationship('Resennas', backref='juego', lazy='dynamic')
 
class TiposUsuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Text)
    comentario = db.Column(db.Text)
    usuarios = db.relationship('Usuarios', backref='tipo_usuario', lazy='dynamic')

class Validado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Text)
    comentario = db.Column(db.Text)
    usuarios = db.relationship('Usuarios', backref='validado', lazy='dynamic')

class Archivos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fichero = db.Column(db.Text)
    comentario = db.Column(db.Text)
    juego_id = db.Column(db.Integer, db.ForeignKey('juegos.id'))

class Usuarios(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    alias = db.Column(db.Text, unique=True)
    nombre = db.Column(db.Text)
    apellidos = db.Column(db.Text)
    telefono = db.Column(db.Text)
    contrasena = db.Column(db.Text)
    email = db.Column(db.Text)
    fecha_creacion = db.Column(db.Text)
    fecha_alta = db.Column(db.Text)
    comentario = db.Column(db.Text)
    id_tipo = db.Column(db.Integer, db.ForeignKey('tipos_usuarios.id'))
    alta = db.Column(db.Integer, db.ForeignKey('validado.id'))

class Resennas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime)
    titulo = db.Column(db.Text)
    detalles = db.Column(db.Text)
    comentario = db.Column(db.Text)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    id_juego = db.Column(db.Integer, db.ForeignKey('juegos.id'))

class Records(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.Text)
    fecha = db.Column(db.DateTime)
    categoria = db.Column(db.Integer)
    video = db.Column(db.Text)
    detalles = db.Column(db.Text)
    comentario = db.Column(db.Text)
    tiempohoras = db.Column(db.Integer)
    tiempominutos = db.Column(db.Integer)
    tiemposegundos = db.Column(db.Integer)
    tiempoms = db.Column(db.Integer)
    idjuego = db.Column(db.Integer)
    idusuario = db.Column(db.Integer)
    idtipo = db.Column(db.Integer)
    records_historico = db.relationship('RecordsHistorico', backref='record', lazy='dynamic')

class RecordsHistorico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posicion = db.Column(db.Text)
    comentario = db.Column(db.Text)
    id_record = db.Column(db.Integer, db.ForeignKey('records.id'))

# Define routes and views
@app.route('/')
def index():
    return render_template('index.html')

# Other routes and views for CRUD operations

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



