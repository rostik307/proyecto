from flask import Blueprint, render_template, flash
views = Blueprint('views',__name__)


@views.route('/',methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@views.route('/puntuaciones',methods=['GET', 'POST'])
def puntuaciones():
    return render_template('puntuaciones.html')


@views.route('/resenas',methods=['GET', 'POST'])
def resenas():
    from . import db
    from .models import Resennas, Juegos, Usuarios

    resennas = db.session.query(Resennas, Juegos, Usuarios).filter(Resennas.id_juego == Juegos.id).filter(Resennas.id_usuario == Usuarios.id).all()
    return render_template('resenas.html', resennas=resennas)



@views.route('/juegos',methods=['GET', 'POST'])
def juegos():
    from . import db
    from .models import Juegos

    juegos = db.session.query(Juegos)
    return render_template('juegos.html', juegos=juegos)

@views.route('/juegos/<int:juego_id>')
def show_juego(juego_id):
    from . import db
    from .models import Juegos, Resennas, Usuarios, Records
    
    juego = Juegos.query.get_or_404(juego_id)
    resennas = db.session.query(Resennas, Usuarios, Juegos).filter(juego_id == Juegos.id == Resennas.id_juego).filter(Resennas.id_usuario == Usuarios.id).filter(Resennas.id_juego == juego.id)
    records = db.session.query(Records, Usuarios, Juegos).filter(juego_id == Juegos.id == Records.idjuego).filter(Records.idusuario == Usuarios.id).filter(Records.idjuego == juego.id)
    return render_template('juego.html', juego=juego, resennas=resennas, records=records)