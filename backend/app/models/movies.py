from typing import List
from threading import Thread
from sqlalchemy import update, event
from datetime import datetime as dt
from .db import Base, SessionLocal, GUID
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, JSON, Text
from slugify import slugify
from time import sleep, time
import uuid, re, json, base64, requests as req
from tinydb import TinyDB, Query
from pprint import pprint
import os

db_nosql = TinyDB('./database/db.json')
db_nosql_2 = TinyDB('./database/db_2.json')

PAGES = int(os.environ['QTD_PAGES'])

db = SessionLocal()

def save_file(path, file):
    with open(f"./json/{path}.json", "w") as f:
        f.write(json.dumps(file))

def jpg_to_base64(link):
    if '.jpg' in link[-4:] and '/' in link[0]:
        img = req.get(f'https://image.tmdb.org/t/p/w154{link}')
        data = base64.b64encode(img.content).decode('utf-8')
        return data

def normalized(string):
    string = slugify(string)
    string = string.replace('-', ' ')
    return string

def get_imdb_info(movie_id):
    try:
        movie_m = MoviesModel.find_by_id(int(movie_id))
        movie_i = MovieInfo.find_by_id(int(movie_id))
            
        if not movie_m or not movie_i:
            raise Exception
        
        movie_m = movie_m.to_json()
        movie_i = movie_i.to_json()
        imdb = dict()
        
        for k in movie_m.keys():
            if k not in imdb:
                imdb[k] = movie_m[k]

        for k in movie_i.keys():
            if k not in imdb:
                imdb[k] = movie_i[k]
    except:
        imdb = None
    
    return movie_m, movie_i, imdb

def download_movie_info(db, url_db, chave_api):
    db_cache = db_nosql_2.all()
    all = MoviesModel.query.all()
    list_all = [i.to_json() for i in all]
    
    data_cache = []
    if list_all and len(db_cache) < (PAGES-1):
        db_nosql_2.truncate()
        for i in list_all:
            try:
                id_imdb = req.get(f"{url_db}/movie/{i['id']}?api_key={chave_api}&language=pt-BR")
                imdb = id_imdb.json()
                if imdb:
                    data_cache.append(imdb)
            except Exception as e:
                print(e)
                continue
        db_nosql_2.insert_multiple(data_cache)
        del data_cache

    db_cache = db_nosql_2.all()
    objects_sql = []
    count = 0
    for imdb in db_cache:
        try:
            if count >= 1:
                db.add_all(objects_sql)
                db.commit()
                print("COMMIT")
                db.close()
                objects_sql = []
                count = 0
            q = MovieInfo.query.filter_by(id=imdb['id']).first()
            if q:
                continue
            db_rec = MovieInfo(**imdb)
            objects_sql.append(db_rec)
            count += 1
        except Exception as e:
            print(e)
            continue

    del objects_sql
    del count
    print("END COMMAND")

def download_database(db, url_db, chave_api):
    # data_first = MoviesModel.query.first()
    data_all = MoviesModel.query.all()

    # print(not data_first, len(data_all) < 1640, len(db_cache) < 82)
    if len(data_all) < 1640:
        db_cache = db_nosql.all()
        if len(db_cache) < (PAGES-1): # and not len(db_cache) == 0:
            db_nosql.truncate()
            
            data_cache = []        
            for i in range(1, PAGES+1):
                try:
                    link = f'{url_db}/trending/movie/week?api_key={chave_api}&language=pt-BR&page={i}&include_adult=true'
                    req_1 = req.get(link)
                    res = req_1.json()
                    if res:
                        data_cache.append(res)
                except:
                    print(e)
                    continue
            db_nosql.insert_multiple(data_cache)
            del data_cache
            db_cache = db_nosql.all()
        print("Caiu Aqui")
        
        count = 0
        objects_sql = []
        for res in db_cache:
            for j in res['results']:
                try:
                    if count >= 1:
                        db.add_all(objects_sql)
                        db.commit()
                        print("COMMIT")
                        db.close()
                        count = 0
                        objects_sql = []
                    q = MoviesModel.query.filter_by(id=j['id']).first()
                    if q:
                        continue
                    objects_sql.append(MoviesModel(**j))
                    count += 1
                except Exception as e:
                    print(f"Exception -- download_database -- db insert -- MoviesModel  {e}")
                    continue
        print("Caiu Aqui 1")
        del objects_sql
        del db_cache
        del count


    # upd = Thread(target=execute_update, args=(db,), daemon=True)
    # upd.start()
    
    upd_2 = Thread(target=download_movie_info, args=(db,url_db, chave_api,), daemon=True)
    upd_2.start()



class MoviesModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    uuid = Column(GUID(), default=uuid.uuid4)
    adult = Column('adult', Boolean)
    backdrop_path = Column('backdrop_path', String)
    backdrop_b64 = Column('backdrop_b64', String)
    genre_ids = Column('genre_ids', JSON)
    original_language = Column('original_language', String)
    original_title = Column('original_title', Text)
    overview = Column('overview', Text)
    poster_path = Column('poster_path', String)
    poster_b64 = Column('poster_b64', String)
    release_date = Column('release_date', String)
    title_norm = Column(Text)
    title = Column('title', Text)
    slug = Column(String)
    video = Column('video', Boolean)
    vote_average = Column('vote_average', Float)
    vote_count = Column('vote_count', Integer)
    popularity = Column('popularity', Float)
    media_type = Column('media_type', String)
    created_at = Column('created_at', DateTime, default=dt.now())
    updated_at = Column('updated_at', DateTime, default=dt.now())

    def __init__(self, *args, **kwargs) -> None:
        self.setAllWithEval(kwargs)

    def setAllWithEval(self, kwargs):
        for key in kwargs.keys():
            if key not in ('uuid', 'created_at', 'updated_at'):
                setattr(self, key, kwargs[key])
    
    def to_json(self):
        return {
            "id": self.id,
            "uuid": f"{self.uuid}",
            "adult": self.adult,
            "backdrop_path": self.backdrop_path,
            "backdrop_b64": self.backdrop_b64,
            "genre_ids": self.genre_ids,
            "original_language": self.original_language,
            "original_title": self.original_title,
            "overview": self.overview,
            "poster_path": self.poster_path,
            "poster_b64": self.poster_b64,
            "release_date": self.release_date,
            "title": self.title,
            "title_norm": self.title_norm,
            "slug": self.slug,
            "video": self.video,
            "vote_average": self.vote_average,
            "vote_count": self.vote_count,
            "popularity": self.popularity,
            "media_type": self.media_type,
            "created_at": f"{self.created_at}",
            "updated_at": f"{self.updated_at}"
        }

    def __repr__(self) -> str:
        return f"MoviesModel(id={self.id}, \
            uuid={self.uuid}, \
            adult={self.adult}, \
            backdrop_path={self.backdrop_path}, \
            backdrop_b64={self.backdrop_b64}, \
            genre_ids={self.genre_ids}, \
            original_language={self.original_language}, \
            original_title={self.original_title}, \
            overview={self.overview}, \
            poster_path={self.poster_path}, \
            poster_b64={self.poster_b64}, \
            release_date={self.release_date}, \
            title={self.title}, \
            title_norm={self.title_norm}, \
            slug={self.slug}, \
            video={self.video}, \
            vote_average={self.vote_average}, \
            vote_count={self.vote_count}, \
            popularity={self.popularity}, \
            media_type={self.media_type}, \
            created_at={self.created_at}, \
            updated_at={self.updated_at})"

    @staticmethod
    def generate_b64_backdrop(target, value, oldvalue, initiator):
        if value and (not target.backdrop_b64 or value != oldvalue):
            target.backdrop_b64 = jpg_to_base64(value)

    @staticmethod
    def generate_b64_poster(target, value, oldvalue, initiator):
        if value and (not target.poster_b64 or value != oldvalue):
            target.poster_b64 = jpg_to_base64(value)

    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)
    
    @staticmethod
    def generate_title_norm(target, value, oldvalue, initiator):
        if value and (not target.title_norm or value != oldvalue):
            target.title_norm = normalized(value)
    
    @classmethod
    def find_by_title(cls, title) -> "MoviesModel":
        return cls.query.filter_by(title=title).first()
    
    @classmethod
    def find_by_id(cls, _id) -> "MoviesModel":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["MoviesModel"]:
        return cls.query.all()
    
    @classmethod
    def find_limit(cls, n) -> List["MoviesModel"]:
        return cls.query.limit(n)
    
    def save_to_db(self) -> None:
        db.add(self)
        db.commit()

    def delete_from_db(self) -> None:
        db.delete(self)
        db.commit()


event.listen(MoviesModel.title, 'set', MoviesModel.generate_slug, retval=False)
event.listen(MoviesModel.title, 'set', MoviesModel.generate_title_norm, retval=False)
event.listen(MoviesModel.poster_path, 'set', MoviesModel.generate_b64_poster, retval=False)
event.listen(MoviesModel.backdrop_path, 'set', MoviesModel.generate_b64_backdrop, retval=False)


class MovieInfo(Base):
    __tablename__ = "movie_info"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    belongs_to_collection = Column(JSON)
    budget = Column(Integer)
    genres = Column(JSON)
    homepage = Column(String)
    imdb_id = Column(String)
    production_companies = Column(JSON)
    production_countries = Column(JSON)
    revenue = Column(Integer)
    runtime = Column(Integer)
    spoken_languages = Column(JSON)
    status = Column(String)
    tagline = Column(Text)
    created_at = Column('created_at', DateTime, default=dt.now())
    updated_at = Column('updated_at', DateTime, default=dt.now())
    
    def __init__(self, *args, **kwargs) -> None:
        self.setAllWithEval(kwargs)

    def setAllWithEval(self, kwargs):
        for key in kwargs.keys():
            if key in (
                'id', \
                'belongs_to_collection', \
                'budget', \
                'genres', \
                'homepage', \
                'imdb_id', \
                'production_companies', \
                'production_countries', \
                'revenue', \
                'runtime', \
                'spoken_languages', \
                'status', \
                'tagline'
            ):
                setattr(self, key, kwargs[key])
    
    def to_json(self):
        return {
            "id": self.id,
            "belongs_to_collection": self.belongs_to_collection,
            "budget": self.budget,
            "genres": self.genres,
            "homepage": self.homepage,
            "imdb_id": self.imdb_id,
            "production_companies": self.production_companies,
            "production_countries": self.production_countries,
            "revenue": self.revenue,
            "runtime": self.runtime,
            "spoken_languages": self.spoken_languages,
            "status": self.status,
            "tagline": self.tagline,
            "created_at": f"{self.created_at}",
            "updated_at": f"{self.updated_at}"
        }
    
    def __repr__(self) -> str:
        return f"MovieInfo(id={self.id}, \
        belongs_to_collection={self.belongs_to_collection}, \
        budget={self.budget}, \
        genres={self.genres}, \
        homepage={self.homepage}, \
        imdb_id={self.imdb_id}, \
        production_companies={self.production_companies}, \
        production_countries={self.production_countries}, \
        revenue={self.revenue}, \
        runtime={self.runtime}, \
        spoken_languages={self.spoken_languages}, \
        status={self.status}, \
        tagline={self.tagline}, \
        created_at={self.created_at}, \
        updated_at={self.updated_at})"
    
    @classmethod
    def find_by_id(cls, _id) -> "MovieInfo":
        return cls.query.filter_by(id=_id).first()
    
    @classmethod
    def find_all(cls) -> List["MovieInfo"]:
        return cls.query.all()
    
    @classmethod
    def find_limit(cls, n) -> List["MovieInfo"]:
        return cls.query.limit(n)
    
    def save_to_db(self) -> None:
        db.add(self)
        db.commit()

    def delete_from_db(self) -> None:
        db.delete(self)
        db.commit()



# def add_data_info(db, *args, **kwargs):
#     if kwargs:
#         all = MoviesModel.query.all()
#         list_all = [i.to_json() for i in all]
#         if list_all:
#             for i in list_all:
#                 try:
#                     db_rec = MovieInfo(**i)
#                     db.add(db_rec)
#                     db.commit()
#                     db.close()
#                 except:
#                     pass
#     else:
#         list_all = args[0]
#         try:
#             if type(list_all) == list:
#                 for i in list_all:
#                     db_rec = MovieInfo(**i)
#                     db.add(db_rec)
#                     db.commit()
#                     db.close()
#             else:
#                 db_rec = MovieInfo(**list_all)
#                 db.add(db_rec)
#                 db.commit()
#                 db.close()
#         except:
#             pass
