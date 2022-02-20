
from jinja2 import pass_context
from app import app

from flask import render_template, request, _app_ctx_stack, jsonify, Response
from ..models.movies import MoviesModel, MovieInfo
from ..models.db import SessionLocal, engine
from sqlalchemy.orm import scoped_session
from threading import Thread, enumerate
from sqlalchemy import text, select
from ..models import movies
from pprint import pprint
from time import sleep

import os, requests, json


app.session= scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
DB = SessionLocal()

API_KEY = os.getenv('API_KEY')
PAGES = int(os.environ['QTD_PAGES'])
URL_DB = 'https://api.themoviedb.org/3'
app.secret_key  = os.getenv('SECRET_KEY')
conn = engine.connect()


@app.before_first_request
def create_tables():
    movies.Base.metadata.create_all(bind=engine)
    dba = Thread(target=movies.download_database, args=(DB, URL_DB, API_KEY,), daemon=True)
    dba.start()


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
        print(f"EXCEPTION: {e}")
        result = []
        for i in range(1, 4):
            try:
                pag = requests.get(f'{URL_DB}/trending/movie/week?api_key={API_KEY}&language=pt-BR&page={i}&include_adult=true')
                json_pag = pag.json()
                result += json_pag['results']
            except:
                if not API_KEY:
                    break
                continue
        if not result:
            return {}, 400
        for i in result:
            i['slug'] = movies.slugify(i['title'])
        resultados_pag1 = result
        x = "req"
        b64 = False
    return render_template('index.html', \
        filmes_pag1=resultados_pag1, \
        busca = resultadosdabusca,
        base64 = b64,
        tipodebusca=x
    )


@app.route("/movie/<movie_id>/<slug>", methods=['GET'])
def movie(movie_id, slug):
    try:
        movie_m, movie_i, imdb = movies.get_imdb_info(movie_id)
        if not movie_m or not movie_i or not imdb:
            raise Exception
    except:
        id_imdb = requests.get(f"{URL_DB}/movie/{movie_id}?api_key={API_KEY}&language=pt-BR")
        imdb = id_imdb.json()
        movies.save_file('movie', imdb)
        try:
            if not movie_m or not movie_i:
                pass
                # try:
                #     dba = Thread(target=movies.insert_to_db, args=(imdb,), daemon=True)
                #     dba.start()
                # except:
                #     pass
            # _, _, imdb = movies.get_imdb_info(movie_id)
        except Exception as e:
            return {"Exception": f"{e}"}, 400
    
    generos = imdb['genres']
    
    try:
        recomendados = MoviesModel.find_by_id(movie_id)
        recomendados = recomendados.to_json()
        recomendados = recomendados['recommended']
        if not recomendados:
            raise Exception
        frecomendados = [i for i in [MoviesModel.find_by_id(j) for j in recomendados] if i]
        if not frecomendados:
            raise Exception
        print("BANCO BANNERS")
    except:
        print("EXCEPTION BANNERS")
        recomendados = requests.get(f"{URL_DB}/movie/{movie_id}/similar?api_key={API_KEY}&language=pt-BR&page=1")
        filmes_recomendados = recomendados.json()
        frecomendados = filmes_recomendados['results']
        for i in frecomendados:
            i['slug'] = movies.slugify(i['title'])
        ids = [i['id'] for i in frecomendados]
        MoviesModel.update_recommended_by_id(_id=movie_id, value=ids)
    
    return render_template('playfilm.html', \
        recomendados = frecomendados, \
        generos = generos, \
        imdb_video = imdb
    )


@app.route("/buscar",methods=['POST'])
def buscar():
    if request.method == "POST":
        buscador = request.form['buscar']    
        try:
            movies_f = MoviesModel.find_by_word(buscador)
            if not movies_f:
                raise Exception
            resultadosdabusca = [i.to_json() for i in movies_f]
            x = 'banco'
            print("Busca Banco")
        except:
            try:
                print("Busca Exception")
                busca = requests.get(f"{URL_DB}/search/movie?api_key={API_KEY}&language=pt-BR&page=1&include_adult=false&query={buscador}")
                buscaEmJson = busca.json()
                # movies.save_file('buscaEmJson', buscaEmJson)
                resultadosdabusca = buscaEmJson['results']
                for i in resultadosdabusca:
                    i['slug'] = movies.slugify(i['title'])
                dba = Thread(target=movies.insert_to_db, args=(resultadosdabusca,), daemon=True)
                dba.start()
                x = 'req'
            except Exception as e:
                print(f"ERRO")
    return render_template('index.html', resultados = resultadosdabusca, tipodebusca=x)


# @app.route("/player",methods=['GET','POST'])
# def player_movie():
#     req = requests.get('https://embed.warezcdn.com/filme/tt6856242')
#     excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
#     # print(req.raw.headers)
#     # headers = [(name, value) for (name, value) in  req.raw.headers.items() if name.lower() not in excluded_headers]
#     headers = [(name, value) for (name, value) in  req.headers.items() if name.lower() not in excluded_headers]
#     res = Response(req.content, req.status_code, headers)
#     # https://embed.warezcdn.com/filme/tt6856242
    
#     return res


# @app.route("/teste/<movie_id>/<slug>",methods=['GET','POST'])
# def teste(movie_id, slug):
#     # result = MoviesModel.query.order_by(MoviesModel.popularity.desc()).limit(60)
#     try:
#         result = MoviesModel.find_by_id(movie_id)
#     except:
#         result = None

#     return render_template('base.html', posts=result)
