import requests as req
import os, json
from pprint import pprint
from app.models.db import SessionLocal, engine
from app.models import movies
from time import sleep
from sqlalchemy import update

import base64


db = SessionLocal()

movies.Base.metadata.create_all(bind=engine)

chave_api = 'f28e3f905e9b24469a4f70b894e618e3'
url_db = 'https://api.themoviedb.org/3'

# req_1 = populares_pag1 = req.get(f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page=2&include_adult=true')
# res = req_1.json()

# with open("lista.json", 'w') as f:
#     f.write(json.dumps(res))
# print(len(res['results']))
# movie_id = 505026
# id_imdb = req.get(f"{url_db}/movie/{movie_id}?api_key={chave_api}&language=pt-BR")
# imdb = id_imdb.json()
# with open("filme.json", 'w') as f:
#     f.write(json.dumps(imdb))

# with open("lista.json", 'r') as f:
#     file = json.loads(f.read())

# for i in range(1, 83):
#     link = f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page={i}&include_adult=true'
#     req_1 = req.get(link)
#     res = req_1.json()
#     try:
#         for j in res['results']:
#             q = db.query(movies.MoviesModel).filter_by(id=j['id']).first()
#             if q:
#                 q = q.to_json()
#                 if j['id'] == q['id']:
#                     continue
#             db_rec = movies.MoviesModel(**j)
#             db.add(db_rec)
#             db.commit()
#     except Exception as e:
#         break
# db.close()
# busca = db.query(movies.MoviesModel).filter(movies.MoviesModel.title.like('mascara%')).limit(15)
# q = db.query(movies.MovieInfo).first()
# pprint(list(busca))
# https://image.tmdb.org/t/p/w154

# img = req.get('https://image.tmdb.org/t/p/w154/odVv1sqVs0KxBXiA8bhIBlPgalx.jpg')
# data = base64.b64encode(img.content).decode('utf-8')
# print(data)


# all = db.query(movies.MoviesModel).all()
# list_all = [i.to_json() for i in all]
# kgnldf = db.query(movies.MoviesModel).update(movies.MoviesModel.backdrop_path).
# print(dir(db.query(movies.MoviesModel).update))

# for i in list_all:
#     if 'jpg' in i['backdrop_path'].split('.')[-1]:
#         db.execute(
#             update(movies.MoviesModel).where(movies.MoviesModel.id == i['id']).values(backdrop_path=movies.jpg_to_base64(i['backdrop_path']))
#         )
#         db.commit()
#         print(i['id'], i['backdrop_path'])
#     if 'jpg' in i['poster_path'].split('.')[-1]:
#         db.execute(
#             update(movies.MoviesModel).where(movies.MoviesModel.id == i['id']).values(poster_path=movies.jpg_to_base64(i['poster_path']))
#         )
#         db.commit()
#         print(i['id'], i['backdrop_path'])
    
    
# /kjWYd2qziS18BPQs85xE6Lb3H09.jpg id=18

# a = movies.MoviesModel.query.first()
all = movies.MoviesModel.query.all()
print([i for i in all])