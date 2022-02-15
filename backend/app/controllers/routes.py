
import os, requests, json
from threading import Thread, enumerate
from requests.api import request
from app import app

from flask import render_template, request, _app_ctx_stack, jsonify
from ..models.movies import MoviesModel, MovieInfo
from ..models.db import SessionLocal, engine
from sqlalchemy.orm import scoped_session
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
    


@app.route("/teste/<movie_id>/<slug>",methods=['GET','POST'])
def teste(movie_id, slug):
    # result = MoviesModel.query.order_by(MoviesModel.popularity.desc()).limit(60)
    try:
        result = MoviesModel.find_by_id(movie_id)
    except:
        result = None

    return render_template('base.html', posts=result)


@app.route("/",methods=['GET','POST'])
def index():
    resultadosdabusca = ""
    try:
        result = MoviesModel.query.order_by(MoviesModel.popularity.desc()).limit(60)
        resultados_pag1 = [i.to_json() for i in result]
        if not resultados_pag1:
            raise Exception
        x = "banco" 
        b64 = True
        print("BANCO")
    except Exception as e:
        print("EXCEPTION")
        result = []
        for i in range(1, 4):
            pag = requests.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            result += json_pag['results']
        for i in result:
            i['slug'] = movies.slugify(i['title'])
        resultados_pag1 = result
        x = "req"
        b64 = False
    # movies.save_file("resultados_pag1", resultados_pag1)
    return render_template('index.html', \
        filmes_pag1=resultados_pag1, \
        busca = resultadosdabusca,
        base64 = b64,
        tipodebusca=x
    )


@app.route("/buscar",methods=['POST'])
def buscar():
    if request.method == "POST":
        buscador = request.form['buscar']    
        # try:
        #     busca = adb.query(movies.MoviesModel).filter(movies.MoviesModel.title.like(f'{buscador}%')).limit(15)
        #     adb.close()
        #     resultadosdabusca = [i.to_json() for i in busca]
        #     if not resultadosdabusca:
        #         raise Exception
        #     x = "banco"     
        # except Exception as e:
        busca = requests.get(f"{url_db}/search/movie?api_key={chave_api}&language=pt-BR&page=1&include_adult=false&query={buscador}")
        buscaEmJson = busca.json()
        resultadosdabusca = buscaEmJson['results']
        for i in resultadosdabusca:
            i['slug'] = movies.slugify(i['title'])
        x = 'req'
    return render_template('index.html', resultados = resultadosdabusca, tipodebusca=x)


@app.route("/movie/<movie_id>/<slug>", methods=['GET'])
def movie(movie_id, slug):
    try:
        movie_m, movie_i, imdb = movies.get_imdb_info(movie_id)
        if not movie_m or not movie_i:
            raise Exception
        # movies.save_file("imdb2", imdb)
    except:
        id_imdb = requests.get(f"{url_db}/movie/{movie_id}?api_key={chave_api}&language=pt-BR")
        imdb = id_imdb.json()
        try:
            if not movie_m:
                db_rec = MoviesModel(**imdb)
                db_rec.save_to_db()
            if not movie_i:
                db_rec = MovieInfo(**imdb)
                db_rec.save_to_db()
            _, _, imdb = movies.get_imdb_info(movie_id)
        except:
            pass
    
    generos = imdb['genres']
    

    recomendados = requests.get(f"{url_db}/movie/{movie_id}/similar?api_key={chave_api}&language=pt-BR&page=1")
    filmes_recomendados = recomendados.json()
    frecomendados = filmes_recomendados['results']
    for i in frecomendados:
        i['slug'] = movies.slugify(i['title'])
    
    
    return render_template('playfilm.html', \
        recomendados = frecomendados, \
        generos = generos, \
        imdb_video = imdb
    )

