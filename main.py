from flask import render_template, redirect, url_for, request
from app import db, Movie, MovieList, app
from manager import DbManager, SearchManager
import subprocess


# db.drop_all()
db.create_all()

db_manager = DbManager()
search_manager = SearchManager()


@app.route("/")
def home():
    all_lists = MovieList.query.all()
    if MovieList.query.filter_by(name="Watched Movies").first():
        all_lists.append(all_lists.pop(all_lists.index(MovieList.query.filter_by(name="Watched Movies").first())))
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


# TODO: change to update all data
@app.route("/edit_mp/", methods=["POST"])
def edit_mp():
    movie_to_update = Movie.query.filter_by(title=request.form["mp_name"]).first()
    movie_to_update.emotional_vibe = request.form["emotional_vibe"]
    movie_to_update.mental_vibe = request.form["mental_vibe"]
    if request.form.getlist('stars'):
        movie_to_update.my_rating = request.form.getlist('stars')[0]
    if request.form.getlist('watched_check'):
        db_manager.add_to_watched_movies(movie_to_update)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/search_movies/<watchlist_id>", methods=["GET", "POST"])
def search_movies(watchlist_id):
    db_manager.current_watchlist = MovieList.query.filter_by(id=watchlist_id).first()
    db_manager.current_id_list = [int(movie.tmdb_id) for movie in db_manager.current_watchlist.movies]
    db_manager.all_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]
    if request.method == "POST":
        search_manager.search_tmdb_titles(title=request.form["search_entry"])
        return render_template("add_movies_page.html",
                               movies=search_manager.movie_titles,
                               shows=search_manager.show_titles,
                               movie_id_list=db_manager.current_id_list,
                               all_ids=db_manager.all_id_list,
                               watchlist=db_manager.current_watchlist)
    return render_template("add_movies_page.html", watchlist=db_manager.current_watchlist)


@app.route("/add_existing_mp/<mp_id>")
def add_existing_mp(mp_id):
    mp = Movie.query.filter_by(tmdb_id=mp_id).first()
    watchlist = MovieList.query.filter_by(id=db_manager.current_watchlist.id).first()
    watchlist.movies.append(mp)
    db.session.commit()
    db_manager.current_id_list = [int(movie.tmdb_id) for movie in watchlist.movies]
    return render_template("add_movies_page.html",
                           movies=search_manager.movie_titles,
                           shows=search_manager.show_titles,
                           movie_id_list=db_manager.current_id_list,
                           all_ids=db_manager.all_id_list,
                           watchlist=db_manager.current_watchlist)


# Adds the movie details to the database sent from select and the vibe-selector form
@app.route("/add-movie", methods=["POST"])
def add_mp():
    search_manager.search_tmdb_details(tmdb_id=request.form["mp_id"], media=request.form["show_movie"])
    # Add the movie to the database
    new_movie = Movie(
        title=search_manager.media_data["title"],
        year=search_manager.media_data["release_date"].split("-")[0],
        description=search_manager.media_data["overview"],
        my_rating=None,
        img_url=f"https://image.tmdb.org/t/p/original{search_manager.media_data['poster_url']}",
        run_time=search_manager.media_data["runtime"],
        pop_rating=round(search_manager.media_data["vote_average"] / 2, 1),
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

    db_manager.current_id_list = [int(movie.tmdb_id) for movie in db_manager.current_watchlist.movies]
    db.all_id_list = [int(movie.tmdb_id) for movie in Movie.query.all()]

    search_manager.added()
    return render_template("add_movies_page.html",
                           movies=search_manager.movie_titles,
                           shows=search_manager.show_titles,
                           movie_id_list=db_manager.current_id_list,
                           all_ids=db_manager.all_id_list,
                           watchlist=db_manager.current_watchlist)


# Deletes a movie
@app.route("/delete_movie/", methods=["POST"])
def delete_movie():
    movie_to_delete = Movie.query.filter_by(title=request.form["movie_name"]).first()
    if request.form.getlist('stars'):
        movie_to_delete.my_rating = request.form.getlist('stars')[0]

    from_watchlist = MovieList.query.filter_by(name=request.form["watchlist_name"]).first()
    from_watchlist.movies.remove(movie_to_delete)

    if request.form.getlist('watched_check'):
        db_manager.add_to_watched_movies(movie_to_delete)

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
    db_manager.get_data(all_movies=Movie.query.all(), all_watchlists=MovieList.query.all())
    if request.method == "POST":
        db_manager.filter_movies(request.form)
        return render_template("movie_picker.html",
                               movies=db_manager.filtered_movies)
    return render_template("movie_picker.html",
                           genres=db_manager.all_genres,
                           watchlists=db_manager.all_watchlists,
                           ave_runtime=round(sum(db_manager.all_runtimes) / len(db_manager.all_runtimes)),
                           max_runtime=max(db_manager.all_runtimes),
                           min_runtime=min(db_manager.all_runtimes))


if __name__ == '__main__':
    subprocess.run('cmd /c start chrome "http://127.0.0.1:5000"')
    app.run(debug=True, use_reloader=False)
