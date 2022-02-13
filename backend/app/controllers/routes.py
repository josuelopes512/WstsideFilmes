
import os, requests
from threading import Thread, enumerate
from requests.api import request
from app import app

from flask import render_template, request, _app_ctx_stack, jsonify
from ..models.db import SessionLocal, engine
from sqlalchemy.orm import scoped_session
from ..models.movies import MoviesModel
from sqlalchemy import text, select
from ..models import movies
from pprint import pprint
from time import sleep

app.session= scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
adb = SessionLocal()

chave_api = os.getenv('API_KEY')
url_db = 'https://api.themoviedb.org/3'
conn = engine.connect()


@app.before_first_request
def create_tables():
    movies.Base.metadata.create_all(bind=engine)
    dba = Thread(target=movies.download_database, args=(adb, url_db, chave_api,), daemon=True)
    dba.start()
    


@app.route("/teste",methods=['GET','POST'])
def teste():
    result = adb.query(MoviesModel).order_by(MoviesModel.popularity.desc()).limit(60)
    result = [i.to_json() for i in result]
    return jsonify(result, f"{enumerate()}")


@app.route("/",methods=['GET','POST'])
def index():
    resultadosdabusca = ""
    try:
        result = adb.query(MoviesModel).order_by(MoviesModel.popularity.desc()).limit(60)
        resultados_pag1 = [i.to_json() for i in result]
        b64 = True
        if not resultados_pag1:
            raise Exception
    except Exception as e:
        result = []
        for i in range(1, 4):
            pag = requests.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            result += json_pag['results']
        resultados_pag1 = result
        b64 = False
    return render_template('index.html', \
        filmes_pag1=resultados_pag1, \
        busca = resultadosdabusca,
        base64 = b64
    )


@app.route("/buscar",methods=['POST'])
def buscar():
    print(request)
    if request.method == "POST":
        buscador = request.form['buscar']    
        try:
            busca = adb.query(movies.MoviesModel).filter(movies.MoviesModel.title.like(f'{buscador}%')).limit(15)
            resultadosdabusca = [i.to_json() for i in busca]
            if not resultadosdabusca:
                raise Exception
            x = "banco"            
        except Exception as e:
            busca = requests.get(f"{url_db}/search/movie?api_key={chave_api}&language=pt-BR&page=1&include_adult=false&query={buscador}")
            buscaEmJson = busca.json()
            resultadosdabusca = buscaEmJson['results']
            x = 'req'
    print(resultadosdabusca, f"{buscador}", x)
    return render_template('index.html', resultados = resultadosdabusca, tipodebusca=x)


@app.route("/movie/<movie_id>", methods=['GET'])
def movie(movie_id):
    id_imdb = requests.get(f"{url_db}/movie/{movie_id}?api_key={chave_api}&language=pt-BR")
    imdb = id_imdb.json()
    generos = imdb['genres']

    recomendados = requests.get(f"{url_db}/movie/{movie_id}/similar?api_key={chave_api}&language=pt-BR&page=1")
    filmes_recomendados = recomendados.json()
    frecomendados = filmes_recomendados['results']
    return render_template('playfilm.html', recomendados = frecomendados,generos = generos,imdb_video = imdb)

