from flask import Flask, render_template, redirect, url_for, request
import requests
from app import db, Movie, MovieList, app
from manager import DbManager, SearchManager
from forms import AddMovieForm, RateMovieForm, NewWatchlistForm

# To do- Wednesday
# TODO: Edit page for movie/manual entry button
# TODO: NavBar
# TODO: Can select page go under the search box?

# To Do - Thursday
# TODO: Add movie picker functionality
# TODO: Add "watched" feature

# To do- Friday
# TODO: Make PRETTY
# TODO: Requirements
# TODO: Make comments on code
# TODO: Make instructional README
# TODO: Download on Jesse's computer
# TODO: Add to Portfolio :)

# Other
# TODO: Same movie different list?
# TODO: trycatch errors: double click


db.create_all()

db_manager = DbManager()
search_manager = SearchManager()

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
        search_manager.search_tmdb_titles(title=add_form.movie.data)
        db_manager.current_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
        return render_template("select.html", movies=search_manager.title_results,
                               movie_id_list=db_manager.current_id_list)
    return render_template("add.html", form=add_form)

# Adds the movie details to the database sent from select
@app.route("/add-movie/<movie_id>")
def add_movie(movie_id):
    search_manager.search_tmdb_details(movie_id)

    # Add the movie to the database
    new_movie = Movie(
        title=search_manager.movie_data["title"],
        year=search_manager.movie_data["release_date"].split("-")[0],
        description=search_manager.movie_data["overview"],
        my_rating=None,
        img_url=f"https://image.tmdb.org/t/p/original{search_manager.movie_data['poster_url']}",
        run_time=search_manager.movie_data["runtime"],
        pop_rating=search_manager.movie_data["vote_average"],
        imdb_id=search_manager.movie_data["imdb_id"],
        watched="False",
        genre=search_manager.movie_data["genre_string"],
        tmdb_id=search_manager.movie_data['id'],
        movie_list=db_manager.current_watchlist
     )

    db.session.add(new_movie)
    db.session.commit()

    db_manager.current_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
    return render_template("select.html", movies=search_manager.title_results,
                           movie_id_list=db_manager.current_id_list)



# Deletes a movie
@app.route("/delete/<movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
