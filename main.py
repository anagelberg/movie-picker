from flask import Flask, render_template, redirect, url_for, request
import requests
import os
from app import db, Movie, MovieList, app
from manager import DbManager

# To do- Wednesday
# TODO: Edit page for movie/manual entry button
# TODO: Make an object to handle some search functionality Manager /clean up code
# TODO: Can select page go under the search box?

# To Do - Thursday
# TODO: Add movie picker functionality

# To do- Friday
# TODO: Make comments on code
# TODO: Make instructional README
# TODO: Download on Jesse's computer
# TODO: Add to Portfolio :)

# Other
# TODO: Same movie different list?
# TODO: trycatch errors: double click

##########################################
TMDB_API_KEY = os.environ['TMDB_API_KEY']
##########################################

db.create_all()
from forms import AddMovieForm, RateMovieForm, NewWatchlistForm

db_manager = DbManager()

@app.route("/")
def home():
    all_lists = MovieList.query.all()
    return render_template("index.html", watchlists=all_lists)

@app.route("/new-movie-list", methods=["GET", "POST"])
def add_list():
    add_form = NewWatchlistForm()
    if add_form.validate_on_submit():
        new_list = MovieList(
            name=add_form.list_name.data,
            description=add_form.description.data
        )
        db.session.add(new_list)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("new_movie_list.html", form=add_form)


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
@app.route("/add/<watchlist_id>", methods=["GET", "POST"])
def add(watchlist_id):
    add_form = AddMovieForm()
    db_manager.current_watchlist = MovieList.query.filter_by(id=watchlist_id).first()
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

        all_movies = Movie.query.all()
        id_list = [int(movie.tmdb_id) for movie in all_movies]
        return render_template("select.html", movies=movie_data, movie_id_list=id_list)
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

    if movie_data["poster_path"] is not None:
        poster_url = movie_data["poster_path"]
    else:
        poster_url = movie_data['belongs_to_collection']['poster_path']

    genre_list = [genre["name"] for genre in movie_data["genres"]]

    # Add the movie to the database
    new_movie = Movie(
        title=movie_data["title"],
        year=movie_data["release_date"].split("-")[0],
        description=movie_data["overview"],
        my_rating=None,
        img_url=f"https://image.tmdb.org/t/p/original{poster_url}",
        run_time=movie_data["runtime"],
        pop_rating=movie_data["vote_average"],
        imdb_id=movie_data["imdb_id"],
        watched="False",
        genre=', '.join(genre_list),
        tmdb_id=movie_data['id'],
        movie_list=db_manager.current_watchlist
     )

    db.session.add(new_movie)
    db.session.commit()

    # TODO: Change this to go to select, first need to make appropriate search manager object?
    return redirect(url_for('home'))



# Deletes a movie
@app.route("/delete/<movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
