from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from sqlalchemy.orm import relationship
from flask_modals import Modal

app = Flask(__name__)
modal = Modal(app)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

# Create in app
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()
Bootstrap(app)


# Create Movie Table
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    my_rating = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(500), nullable=True)
    pop_rating = db.Column(db.Float, nullable=True)
    run_time = db.Column(db.Integer, nullable=True)
    genre = db.Column(db.String(200), nullable=True)
    watched = db.Column(db.String(10), nullable=False)
    imdb_id = db.Column(db.String(30), nullable=True)
    tmdb_id = db.Column(db.String(50), nullable=False)
    emotional_vibe = db.Column(db.String(20), nullable=False)
    mental_vibe = db.Column(db.String(20), nullable=False)
    movie_list = relationship("MovieList", back_populates="movies")
    movie_list_id = db.Column(db.Integer, db.ForeignKey('movie_lists.id'))


# Create Movie List Table
class MovieList(db.Model):
    __tablename__ = "movie_lists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=True)
    movies = relationship("Movie", back_populates="movie_list")
