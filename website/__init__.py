from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "juegarapido.db"


def initialize_database():
    from . import db
    from .models import Juegos, CategoriasJuegos, CategoriasRecords, Resennas, Usuarios, Records
    import datetime
    from werkzeug.security import generate_password_hash

    def insert_game(nombre,fecha,imagen,categoria_id):

        newgame = Juegos(
            nombre = nombre,
            fecha = datetime.datetime.strptime(fecha, f'%Y-%m-%d %H:%M'),
            imagen = imagen,
            categoria_id = categoria_id,
        )

        game_verified = Juegos.query.filter_by(nombre=nombre).first()
        if not game_verified:
            db.session.add(newgame)
            db.session.commit()
        else:
            print('no introducido el juego '+newgame.nombre+' porque ya estaba en la bbdd')
    
    def insert_game_category(id,nombre,descripcion):

        newgamecat = CategoriasJuegos(
            id = id,
            nombre = nombre,
            descripcion = descripcion,
        )

        cat_verifiedid = CategoriasJuegos.query.filter_by(id=id).first()
        cat_verifiedname = CategoriasJuegos.query.filter_by(nombre=nombre).first()

        if not (cat_verifiedid and cat_verifiedname):
            db.session.add(newgamecat)
            db.session.commit()
        elif not cat_verifiedid:
            print('no introducida la categoria de juegos '+newgamecat.nombre+' porque el id estaba repetido')
        else: 
            print('no introducida la categoria de juegos '+newgamecat.nombre+' porque ya estaba en la bbdd')

    def insert_record_category(id,nombre,descripcion):
        newreccat = CategoriasRecords(
            id = id,
            nombre = nombre,
            descripcion = descripcion,
        )
        
        cat_verifiedid = CategoriasRecords.query.filter_by(id=id).first()
        cat_verifiedname = CategoriasRecords.query.filter_by(nombre=nombre).first()
        
        if not (cat_verifiedid and cat_verifiedname):
            db.session.add(newreccat)
            db.session.commit()
        elif not cat_verifiedid:
            print('no introducida la categoria de records '+newreccat.nombre+' porque el id estaba repetido')
        else: 
            print('no introducida la categoria de records '+newreccat.nombre+' porque ya estaba en la bbdd')

    def insert_User(alias, nombre, apellidos, telefono, contrasena, email, comentario, id_tipo):
        newuser = Usuarios(
            alias = alias,
            nombre = nombre,
            apellidos = apellidos,
            telefono = telefono,
            email = email,
            comentario = comentario,
            id_tipo = id_tipo,
            contrasena = generate_password_hash(contrasena, method='pbkdf2:sha256'),
        )

        rev_verifiedname = Usuarios.query.filter_by(alias=alias).first()
        rev_verifiedmail = Usuarios.query.filter_by(email=email).first()

        if not (rev_verifiedname and rev_verifiedmail):
            db.session.add(newuser)
            db.session.commit()
        elif not rev_verifiedname:
            print('no introducido el usuario '+newuser.alias+' porque el alias estaba repetido')
        elif not rev_verifiedmail:
            print('no introducido el usuario con email '+newuser.email+' porque el correo estaba repetido')
        else: 
            print('no introducido el usuario '+newuser.alias+' porque ya estaba en la bbdd')
        

    def insert_reviews(fecha,titulo,detalles,comentario,id_usuario,id_juego):
        newrev = Resennas(
            fecha = datetime.datetime.strptime(fecha, f'%Y-%m-%d %H:%M'),
            titulo = titulo,
            detalles = detalles,
            comentario = comentario,
            id_usuario = id_usuario,
            id_juego = id_juego,
        )

        rev_verifiedtitle = Resennas.query.filter_by(titulo = titulo).first()
        rev_verifiedcomment = Resennas.query.filter_by(detalles = detalles).first()

        if not (rev_verifiedtitle and rev_verifiedcomment):
            db.session.add(newrev)
            db.session.commit()
        else:
            print('no introducida la reseña '+newrev.titulo+' porque está repetida')


    def insert_record(titulo,detalles,fecha,video,tiempo_horas,tiempo_minutos,tiempo_segundos,tiempo_ms,id_usuario,id_juego,id_tipo,comentario):
        newrec = Records(
            fecha = datetime.datetime.strptime(fecha, f'%Y-%m-%d %H:%M'),
            titulo = titulo,
            detalles = detalles,
            video = video,
            tiempohoras = tiempo_horas,
            tiempominutos = tiempo_minutos,
            tiemposegundos = tiempo_segundos,
            tiempoms = tiempo_ms,
            idusuario = id_usuario,
            idjuego = id_juego,
            idtipo = id_tipo,
            comentario = comentario,
        )

        rec_verifieduser = Records.query.filter_by(idusuario = id_usuario).first()
        rec_verifiedtitle = Records.query.filter_by(titulo = titulo).first()
        rec_verifiedcomment = Records.query.filter_by(detalles = detalles).first()

        if (rec_verifieduser and rec_verifiedtitle and rec_verifiedcomment):
            print('no introducido el record '+newrec.titulo+' porque está repetido')
        else:
            db.session.add(newrec)
            db.session.commit()

        

    current_date = datetime.datetime.now()
    date_time = current_date.strftime(f"%Y-%m-%d %H:%M")

    insert_game_category(1,'terror','juegos de miedo')
    insert_game_category(2,'shooter','juegos de disparos')
    insert_game_category(3, 'adventure', 'juegos de aventura')
    insert_game_category(4, 'role-playing', 'juegos de rol')
    insert_game_category(5, 'sports', 'juegos de deportes')
    insert_game_category(6, 'strategy', 'juegos de estrategia')
    insert_game_category(7, 'puzzle', 'juegos de rompecabezas')
    insert_game_category(8, 'platformer', 'juegos de plataformas')
    insert_game_category(9, 'fighting', 'juegos de lucha')
    insert_game_category(10, 'racing', 'juegos de carreras')
    insert_game_category(11, 'sandbox', 'juegos de mundo abierto')
    insert_game_category(12, 'simulation', 'juegos de simulación')
    insert_game_category(13, 'educational', 'juegos educativos')
    insert_game_category(14, 'music', 'juegos musicales')
    insert_game_category(15, 'arcade', 'juegos arcade')
    insert_game_category(16, 'stealth', 'juegos de sigilo')
    insert_game_category(17, 'horror', 'juegos de terror')
    insert_game_category(18, 'fantasy', 'juegos de fantasía')
    insert_game_category(19, 'sci-fi', 'juegos de ciencia ficción')
    insert_game_category(20, 'mystery', 'juegos de misterio')


    insert_game('Dustforce','2014-10-09 00:00','dustforce.png',8)
    insert_game('Minecraft',date_time,'minecraft.png',3)
    insert_game('Super Mario 64',date_time,'img2.png',8)
    insert_game('Example 1',date_time,'img2.png',1)
    insert_game('Example 2',date_time,'img3.png',2)
    insert_game('Example 3',date_time,'img3.png',4)
    insert_game('Example 4',date_time,'img3.png',5)
    insert_game('Example 5',date_time,'img3.png',6)
    insert_game('Example 6',date_time,'img3.png',7)
    insert_game('Example 7',date_time,'img3.png',9)
    insert_game('Example 8',date_time,'img3.png',10)
    insert_game('Example 9',date_time,'img3.png',11)

    insert_record_category(1,'any %','completar el juego de la forma más rapida posible')
    insert_record_category(2,r'any % glitchless', 'completar el juego lo mas rapido posible sin usar glitches')
    insert_record_category(3,'100%',r'completar el juego al 100% lo mas rapido posible')
    insert_record_category(4,'no hit','completar el juego sin ser golpeado lo mas rapido posible')
    insert_record_category(5,'tutorial','completar el tutorial lo mas rapido posible')
    
    insert_User('aaa','aaa','aaa','123456789','aaa','aaa@aaa.aaa','',1)
    insert_User('test','test','test','123456789','test','example1@a.com','',1)
    insert_User('user','user','user','123456789','user','example2@a.com','',1)
    insert_User('admin','admin','admin','123456789','admin','admin@a.com','',2)

    insert_reviews(date_time,'Review Test 1','esta review es una prueba, el usuario debe de ser "aaa" y debe de ser una review de minecraft','',1,2)
    insert_reviews(date_time,'Review Test 2','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 3','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 4','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 5','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 6','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 7','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 8','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 9','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)
    insert_reviews(date_time,'Review Test 10','esta review es una prueba, el usuario debe de ser "test" y debe de ser una review de dustforce','',2,1)

    insert_record('dustforce any% tutorial WR','current world record in the tutorial level',date_time,'youtu.be/abc12345678',0,1,15,100,1,1,5,'')
    insert_record('dustforce any%','run for the game',date_time,'youtu.be/abc12345678',1,2,45,33,2,1,1,'')
    insert_record('minecraft any%','run for the game',date_time,'youtu.be/abc12345678',1,2,45,33,2,2,1,'')
    insert_record('minecraft any% WR','run for the game',date_time,'youtu.be/abc12345678',1,2,45,32,2,2,1,'')

def create_app():
    from .views import views
    from .auth import auth

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import Usuarios
    
    with app.app_context():
        db.create_all()
        initialize_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Usuarios.query.get(int(id))

    return app

def create_database(app):
    
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        initialize_database()


#===============================================================================
