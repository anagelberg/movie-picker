from flask import Flask, render_template, redirect, url_for, request
import requests
from app import db, Movie, MovieList, app, modal
from manager import DbManager, SearchManager
from forms import SearchMovieForm, RateMovieForm
from flask_modals import render_template_modal


# NECESSARY
# TODO: !Add "watched" feature / own list
# TODO: !Edit page for movie/manual entry button
# TODO: (begin_) Make PRETTY
# TODO: !Same movie different list?


# Nice-to-haves
# TODO: trycatch errors: double click
# TODO: Try TV show search
# TODO: talk to letterboxd


# When ready to publish: FRIDAY
# TODO: Requirements file
# TODO: Make comments on code
# TODO: Make instructional README
# TODO: Download on Jesse's computer
# TODO: Add to Portfolio :)

db.create_all()

db_manager = DbManager()
search_manager = SearchManager()


@app.route("/")
def home():
    all_lists = MovieList.query.all()
    return render_template("index.html", watchlists=all_lists)


@app.route("/new-movie-list", methods=["POST"])
def add_list():
    new_list = MovieList(
        name=request.form["watchlist_name"],
        description=request.form["watchlist_description"]
        )
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/create-list")
def create_list():
    return render_template("add_new_movie_jar.html")

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

@app.route("/show_search_screen/<watchlist_id>")
def show_search_screen(watchlist_id):
    db_manager.current_watchlist = MovieList.query.filter_by(id=watchlist_id).first()
    db_manager.current_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
    return render_template("search_movie_titles.html")


@app.route("/select-movie", methods=["POST"])
def select_movie():
    search_manager.search_tmdb_titles(title=request.form["search_entry"])
    return render_template("select.html", movies=search_manager.title_results,
                           movie_id_list=db_manager.current_id_list)


@app.route("/select_vibe/<movie_id>", methods=["GET", "POST"])
def select_vibe(movie_id):
    search_manager.movie_id_to_add = movie_id
    return render_template_modal("vibe_selector.html")


# Adds the movie details to the database sent from select and the vibe-selector form
@app.route("/add-movie", methods=["POST"])
def add_movie():
    search_manager.search_tmdb_details(search_manager.movie_id_to_add)

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
        movie_list=db_manager.current_watchlist,
        emotional_vibe=request.form['emotional_vibe'],
        mental_vibe=request.form['mental_vibe']
    )

    db.session.add(new_movie)
    db.session.commit()

    db_manager.current_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
    search_manager.added()
    return render_template("select.html", movies=search_manager.title_results,
                           movie_id_list=db_manager.current_id_list)


# Deletes a movie
@app.route("/delete/<movie_id>")
def delete(movie_id):
    movie_to_delete = Movie.query.filter_by(id=movie_id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/movie_jar", methods=["GET", "POST"])
def movie_jar():
    # TODO: make max runtime dynamic
    # TODO: add genres into it
    db_manager.get_data(all_movies=Movie.query.all(), all_watchlists=MovieList.query.all())
    if request.method == "POST":
        db_manager.filter_movies(request.form)
        return render_template("movie_jar.html",
                               movies=db_manager.filtered_movies)
    return render_template("movie_jar.html",
                           genres=db_manager.all_genres,
                           watchlists=db_manager.all_watchlists)


@app.route("/test", methods=["GET", "POST"])
def test():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
