import os
from requests.api import request
from app import app
import requests
from flask import render_template,request


chave_api = os.environ['API_KEY']
url_db = 'https://api.themoviedb.org/3'


@app.route("/",methods=['GET','POST'])
def index():
#  chave_api  =  Adicinar a chave da api
    populares_pag1 = requests.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page=1&include_adult=true')
    populares_pag2 = requests.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page=2&include_adult=true')
    populares_pag3 = requests.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page=3&include_adult=true')
    json_pag1 = populares_pag1.json()
    json_pag2 = populares_pag2.json()
    json_pag3 = populares_pag3.json()
    resultados_pag1 = json_pag1['results']
    resultados_pag2 = json_pag2['results']
    resultados_pag3 = json_pag3['results']
    resultadosdabusca = ""
    
    return render_template('index.html', \
      filmes_pag1=resultados_pag1, \
      filmes_pag2 = resultados_pag2, \
      filmes_pag3 = resultados_pag3, \
      busca = resultadosdabusca
    )

@app.route("/buscar",methods=['POST'])
def buscar():
#  chave_api  =  Adicinar a chave da api
    if request.method == "POST":
        buscador = request.form['buscar']
        # print(buscador)
        busca = requests.get(f"{url_db}/search/movie?api_key={chave_api}&language=pt-BR&page=1&include_adult=false&query={buscador}")
        buscaEmJson = busca.json()
        resultadosdabusca = buscaEmJson['results']

    return render_template('index.html', resultados = resultadosdabusca)

@app.route("/movie/<movie_id>", methods=['GET'])
def movie(movie_id):
#  chave_api  =  Adicinar a chave da api
    id_imdb = requests.get(f"{url_db}/movie/{movie_id}?api_key={chave_api}&language=pt-BR")
    imdb = id_imdb.json()
    generos = imdb['genres']

    recomendados = requests.get(f"{url_db}/movie/{movie_id}/similar?api_key={chave_api}&language=pt-BR&page=1")
    filmes_recomendados = recomendados.json()
    frecomendados = filmes_recomendados['results']
    return render_template('playfilm.html', recomendados = frecomendados,generos = generos,imdb_video = imdb)

