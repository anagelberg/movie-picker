from flask import render_template, redirect, url_for, request
from app import db, Movie, MovieList, app
from manager import DbManager, SearchManager


# NECESSARY
# TODO: (begin_) Make PRETTY

# Nice-to-haves
# TODO: talk to letterboxd

# When ready to publish: FRIDAY
# TODO: Requirements file
# TODO: Make comments on code
# TODO: Make instructional README
# TODO: Download on Jesse's computer
# TODO: Add to Portfolio :)

#db.drop_all()
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

@app.route("/show-edit-page/<movie_id>")
def show_edit_page(movie_id):
    db_manager.movie_to_update = Movie.query.filter_by(id=movie_id).first()
    return render_template("edit.html", movie=db_manager.movie_to_update)

# TODO: change to update all data
@app.route("/edit/", methods=["POST"])
def edit():
    movie_to_update = Movie.query.filter_by(id=db_manager.movie_to_update.id).first()
    movie_to_update.title = request.form["title"]
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/show_search_screen/<watchlist_id>")
def show_search_screen(watchlist_id):
    db_manager.current_watchlist = MovieList.query.filter_by(id=watchlist_id).first()
    db_manager.current_id_list = [int(movie.tmdb_id) for movie in db_manager.current_watchlist.movies]
    return render_template("search_movie_titles.html")


@app.route("/select-movie", methods=["POST"])
def select_movie():
    search_manager.search_tmdb_titles(title=request.form["search_entry"])
    return render_template("select.html", movies=search_manager.movie_titles,
                           shows=search_manager.show_titles,
                           movie_id_list=db_manager.current_id_list)


@app.route("/select_vibe/<movie_id>/<tv_or_movie>", methods=["GET", "POST"])
def select_vibe(movie_id, tv_or_movie):
    movie_check = Movie.query.filter_by(tmdb_id=movie_id).first()
    search_manager.show_or_movie = tv_or_movie
    if movie_check:
        watchlist = MovieList.query.filter_by(id=db_manager.current_watchlist.id).first()
        watchlist.movies.append(movie_check)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        search_manager.movie_id_to_add = movie_id
        return render_template("vibe_selector.html")


# Adds the movie details to the database sent from select and the vibe-selector form
@app.route("/add-movie", methods=["POST"])
def add_movie():
    search_manager.search_tmdb_details(tmdb_id=search_manager.movie_id_to_add, media=search_manager.show_or_movie)

    # Add the movie to the database
    new_movie = Movie(
        title=search_manager.media_data["title"],
        year=search_manager.media_data["release_date"].split("-")[0],
        description=search_manager.media_data["overview"],
        my_rating=None,
        img_url=f"https://image.tmdb.org/t/p/original{search_manager.media_data['poster_url']}",
        run_time=search_manager.media_data["runtime"],
        pop_rating=search_manager.media_data["vote_average"],
        imdb_id=search_manager.media_data["imdb_id"],
        watched="False",
        genre=search_manager.media_data["genre_string"],
        tmdb_id=search_manager.media_data['id'],
        emotional_vibe=request.form['emotional_vibe'],
        mental_vibe=request.form['mental_vibe']
    )

    new_movie.movie_list.append(db_manager.current_watchlist)

    db.session.add(new_movie)
    db.session.commit()

    db_manager.current_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
    search_manager.added()
    return render_template("select.html",   movies=search_manager.movie_titles,
                                            shows=search_manager.show_titles,
                                            movie_id_list=db_manager.current_id_list)


# Deletes a movie
@app.route("/delete_movie/", methods=["POST"])
def delete_movie():
    movie_to_delete = Movie.query.filter_by(title=request.form["movie_name"]).first()
    if request.form.getlist('stars'):
        movie_to_delete.my_rating = request.form.getlist('stars')[0]

    from_watchlist = MovieList.query.filter_by(name=request.form["watchlist_name"]).first()
    from_watchlist.movies.remove(movie_to_delete)

    if request.form.getlist('watched_check'):
        movie_to_delete.watched = "True"
        watched_list = MovieList.query.filter_by(name="Watched Movies").first()
        if not watched_list:
            watched_list = MovieList(
                name="Watched Movies",
                description="These are the movies you've seen."
            )
            db.session.add(watched_list)
        movie_to_delete.movie_list.append(watched_list)

    db.session.commit()
    return redirect(url_for('home'))

# Deletes a movie
@app.route("/delete_movie_list/<watchlist_id>")
def delete_movie_list(watchlist_id):
    watchlist_to_delete = MovieList.query.filter_by(id=watchlist_id).first()
    db.session.delete(watchlist_to_delete)
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
