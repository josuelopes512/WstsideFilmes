from .db import Base, SessionLocal, UUID

from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, JSON, Text
from sqlalchemy.types import Date, TypeDecorator, CHAR


from typing import List
from datetime import datetime as dt
import uuid, re, json, base64, requests as req

from threading import Thread

db = SessionLocal()
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.
    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                # hexstring
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

def slugify(text):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', text)

def jpg_to_base64(link):
    if '.jpg' in link:
        img = req.get(f'https://image.tmdb.org/t/p/w154{link}')
        data = base64.b64encode(img.content).decode('utf-8')
        return data
    return link

class MoviesModel(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    uuid = Column(GUID(), default=uuid.uuid4)
    adult = Column('adult', Boolean)
    backdrop_path = Column('backdrop_path', String)
    genre_ids = Column('genre_ids', JSON)
    # id_movie = Column('id_movie', Integer)
    original_language = Column('original_language', String)
    original_title = Column('original_title', Text)
    overview = Column('overview', Text)
    poster_path = Column('poster_path', String)
    release_date = Column('release_date', String)
    title = Column('title', Text)
    video = Column('video', Boolean)
    vote_average = Column('vote_average', Float)
    vote_count = Column('vote_count', Integer)
    popularity = Column('popularity', Float)
    media_type = Column('media_type', String)
    created_at = Column('created_at', DateTime, default=dt.now())
    updated_at = Column('updated_at', DateTime, default=dt.now())

    def __init__(self, *args, **kwargs) -> None:
        self.setAllWithEval(kwargs)
        self.generate_slug()
        # self.convert_to_base64()

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
            "genre_ids": self.genre_ids,
            "original_language": self.original_language,
            "original_title": self.original_title,
            "overview": self.overview,
            "poster_path": self.poster_path,
            "release_date": self.release_date,
            "title": self.title,
            "video": self.video,
            "vote_average": self.vote_average,
            "vote_count": self.vote_count,
            "popularity": self.popularity,
            "media_type": self.media_type,
            "created_at": f"{self.created_at}",
            "updated_at": f"{self.updated_at}"
        }

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title.lower())
        else:
            self.slug = str(self.uuid).lower()
    
    def convert_to_base64(self):
        if self.backdrop_path:
            self.backdrop_path = jpg_to_base64(self.backdrop_path)
        if self.poster_path:
            self.poster_path = jpg_to_base64(self.poster_path)
    
    def __repr__(self) -> str:
        return f"MoviesModel(id={self.id}, \
            uuid={self.uuid}, \
            adult={self.adult}, \
            backdrop_path={self.backdrop_path}, \
            genre_ids={self.genre_ids}, \
            original_language={self.original_language}, \
            original_title={self.original_title}, \
            overview={self.overview}, \
            poster_path={self.poster_path}, \
            release_date={self.release_date}, \
            title={self.title}, \
            video={self.video}, \
            vote_average={self.vote_average}, \
            vote_count={self.vote_count}, \
            popularity={self.popularity}, \
            media_type={self.media_type}, \
            created_at={self.created_at}, \
            updated_at={self.updated_at})"
    
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
                'tagline', \
                'created_at', \
                'updated_at'
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
            "created_at": self.created_at,
            "updated_at": self.updated_at
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

