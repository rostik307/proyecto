from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user
from urllib.parse import urlparse, parse_qs
import datetime

views = Blueprint('views',__name__)

def get_video_id(youtube_url):
    url_components = urlparse(youtube_url)
    if url_components.hostname in ['www.youtube.com', 'youtube.com']:
        if url_components.path == '/watch':
            query = parse_qs(url_components.query)
            return query.get('v', [None])[0]
        elif url_components.path.startswith('/embed/'):
            return url_components.path.split('/')[2]
        elif url_components.path.startswith('/v/'):
            return url_components.path.split('/')[2]
    elif url_components.hostname in ['youtu.be']:
        return url_components.path[1:]
    return None

@views.route('/',methods=['GET', 'POST'])
def home():
    from . import db
    from .models import Juegos
    
    juegos = db.session.query(Juegos)
    return render_template('home.html',juegos=juegos)


@views.route('/puntuaciones',methods=['GET', 'POST'])
def puntuaciones():
    return render_template('puntuaciones.html')


@views.route('/resenas',methods=['GET', 'POST'])
def resenas():
    from . import db
    from .models import Resennas, Juegos, Usuarios

    if request.method == 'POST':
        idjuego = request.form.get('game')
        idusuario = current_user.id
        titulo = request.form.get('title')
        descripcion = request.form.get('desc')
        current_date = datetime.datetime.now()

        new_record = Resennas(
            titulo = titulo,
            fecha = current_date,
            detalles = descripcion,
            id_usuario = idusuario,
            id_juego = idjuego,
            )
        db.session.add(new_record)
        db.session.commit()
        flash('Record registrado!', category='success')
        return redirect(url_for('views.records'))

    juegos = db.session.query(Juegos)
    resennas = db.session.query(Resennas, Juegos, Usuarios).filter(Resennas.id_juego == Juegos.id).filter(Resennas.id_usuario == Usuarios.id).all()
    return render_template('resenas.html', resennas=resennas, juegos=juegos)



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

@views.route('/records',methods=['GET', 'POST'])
def records():
    from . import db
    from .models import Records
    if request.method == 'POST':
        idjuego = request.form.get('game')
        idcategoria = request.form.get('category')
        idusuario = current_user.id
        titulo = request.form.get('title')
        descripcion = request.form.get('desc')
        video = get_video_id(request.form.get('video'))
        tiempohoras = request.form.get('horas')
        tiempominutos = request.form.get('minutos')
        tiemposegundos = request.form.get('segundos')
        tiempoms = request.form.get('ms')

        current_date = datetime.datetime.now()

        new_record = Records(
            titulo = titulo,
            fecha = current_date,
            video = video,
            detalles = descripcion,
            tiempohoras = tiempohoras,
            tiempominutos = tiempominutos,
            tiemposegundos = tiemposegundos,
            tiempoms = tiempoms,
            idjuego = idjuego,
            idusuario = idusuario,
            idtipo = idcategoria,
            )
        db.session.add(new_record)
        db.session.commit()
        flash('Record registrado!', category='success')
        return redirect(url_for('views.records'))
        
    from . import db
    from .models import Juegos, Records, Usuarios, CategoriasRecords

    juegos = db.session.query(Juegos)
    categorias = db.session.query(CategoriasRecords)
    records = db.session.query(Records,Usuarios,Juegos).filter(Usuarios.id == Records.idusuario).filter(Juegos.id == Records.idjuego)
    return render_template('records.html', records=records,juegos=juegos,catrec=categorias)



@views.route('/record/<int:record_id>')
def show_record(record_id):
    from . import db
    from .models import Juegos, Usuarios, Records

    record = Records.query.get_or_404(record_id)
    records = db.session.query(Records, Usuarios, Juegos).filter(Records.idusuario == Usuarios.id).filter(Records.id == record_id)

    
    return render_template('record.html',record=record, records=records)