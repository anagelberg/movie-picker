from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


class AddMovieForm(FlaskForm):
    movie = StringField(label='Movie Title', validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")

class RateMovieForm(FlaskForm):
    my_rating = StringField(label='Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    submit = SubmitField(label="Done")


TMDB_API_KEY = "bba491762ee6540f2a2e380a224c0979"


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()

Bootstrap(app)


# Create Movie Table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    my_rating = db.Column(db.Float, nullable=True)
    img_url = db.Column(db.String(500), nullable=False)
    critic_rating = db.Column(db.Float, nullable=True)
    run_time = db.Column(db.Float, nullable=True)
    genre = db.Column(db.String(200), nullable=True)
    on_netflix = db.Column(db.String(10), nullable=True)
    on_amazon = db.Column(db.String(10), nullable=True)
    on_disney = db.Column(db.String(10), nullable=True)
    on_hulu = db.Column(db.String(10), nullable=True)
    youtube_rental_price = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Book {self.title}>'

    def update_stream_availability_data(self):
        pass


db.create_all()

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.critic_rating).all()
    return render_template("index.html", movies=all_movies)

# Edit rating
@app.route("/edit/<movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    edit_form = RateMovieForm()
    movie_to_update = Movie.query.filter_by(id=movie_id).first()
    if edit_form.validate_on_submit():
        movie_to_update.my_rating = edit_form.my_rating.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=edit_form, movie=movie_to_update)


# Form to add movie, searches based on title and sends to select page
@app.route("/add", methods=["GET", "POST"])
def add():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.movie.data
        parameters = {
            'api_key': TMDB_API_KEY,
            'language': 'en-US',
            'query': movie_title,
        }
        response = requests.get(url='https://api.themoviedb.org/3/search/movie', params=parameters)
        response.raise_for_status()
        data = response.json()
        movie_data = data['results']
        return render_template("select.html", movies=movie_data)
    return render_template("add.html", form=add_form)

# Adds the movie details to the database sent from select
@app.route("/add-movie/<movie_id>")
def add_movie(movie_id):
    parameters = {
        'api_key': TMDB_API_KEY,
    }
    response = requests.get(url=f'https://api.themoviedb.org/3/movie/{movie_id}', params=parameters)
    response.raise_for_status()
    movie_data = response.json()


    # Add the movie to the database
    if movie_data["poster_path"] is not None:
        poster_url = movie_data["poster_path"]
    else:
        poster_url = movie_data['belongs_to_collection']['poster_path']


    new_movie = Movie(
        title=movie_data["title"],
        year=movie_data["release_date"],
        description=movie_data["overview"],
        my_rating=None,
        img_url=f"https://image.tmdb.org/t/p/original{poster_url}",
        run_time=None
     )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("edit", movie_id=new_movie.id))



# Deletes a movie
@app.route("/delete/<movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
