import os
import requests


class DbManager:
    def __init__(self):
        self.filtered_movies = None
        self.current_watchlist = None
        self.current_id_list = []
        self.movie_id_to_add = None
        self.all_genres = []
        self.all_watchlists = None
        self.movie_to_update = None
        self.all_id_list = []
        self.all_runtimes = None

    def get_data(self, all_movies, all_watchlists):
        for movie in all_movies:
            for genre in movie.genre.split(","):
                if genre.strip() not in self.all_genres:
                    self.all_genres.append(genre.strip())
        self.all_watchlists = [li.name for li in all_watchlists]
        self.all_runtimes = [movie.run_time for movie in all_movies]

    def filter_movies(self, form_data):
        from app import Movie, MovieList
        pre_filtered_movies = Movie.query.filter(Movie.run_time <= form_data["max_runtime"],
                                                 Movie.emotional_vibe.in_(form_data.getlist('emotional_vibe')),
                                                 Movie.mental_vibe.in_(form_data.getlist('mental_vibe')),
                                                 Movie.id.in_([movie.id for movie in MovieList.query.filter_by(
                                                     name=form_data["movie_list_dropdown"]).first().movies])).all()

        self.filtered_movies = []
        for movie in pre_filtered_movies:
            if any(genre in movie.genre for genre in form_data.getlist("genre_selection")):
                self.filtered_movies.append(movie)
        self.filtered_movies.sort(key=lambda x: x.pop_rating, reverse=True)  # sort descending

    def add_to_watched_movies(self, movie):
        from app import Movie, MovieList, db
        watched_list = MovieList.query.filter_by(name="Watched Movies").first()
        movie.watched = "True"
        if not watched_list:
            watched_list = MovieList(
                name="Watched Movies",
                description="These are the movies you've seen."
            )
            db.session.add(watched_list)
            watched_movies = Movie.query.filter(Movie.watched == "True").all()
            for movie in watched_movies:
                watched_list.movies.append(movie)
        movie.movie_list.append(watched_list)
        db.session.commit()



class SearchManager:
    def __init__(self):
        self.show_titles = None
        self.movie_titles = None
        self.media_data = None
        self.movie_id_to_add = None
        self.TMDB_API_KEY = os.environ['TMDB_API_KEY']

    def search_tmdb_titles(self, title):
        parameters = {
            'api_key': self.TMDB_API_KEY,
            'language': 'en-US',
            'query': title,
        }
        # Search movies
        response = requests.get(url='https://api.themoviedb.org/3/search/movie', params=parameters)
        response.raise_for_status()
        data = response.json()
        self.movie_titles = data['results']

        # Search TV shows
        response = requests.get(url='https://api.themoviedb.org/3/search/tv', params=parameters)
        response.raise_for_status()
        data = response.json()
        self.show_titles = data['results']


    def search_tmdb_details(self, tmdb_id, media="movie"):
        parameters = {
            'api_key': self.TMDB_API_KEY,
        }
        response = requests.get(url=f'https://api.themoviedb.org/3/{media}/{tmdb_id}', params=parameters)
        response.raise_for_status()
        self.media_data = response.json()

        if self.media_data["poster_path"]:
            self.media_data["poster_url"] = self.media_data["poster_path"]
        elif self.media_data['belongs_to_collection']:
            self.media_data["poster_url"] = self.media_data['belongs_to_collection']['poster_path']
        else:
            self.media_data["poster_url"] = None

        genre_list = [genre["name"] for genre in self.media_data["genres"]]
        self.media_data["genre_string"] = ', '.join(genre_list)

        if media == "tv":
            self.media_data["runtime"] = round(sum(
                self.media_data["episode_run_time"])/len(self.media_data["episode_run_time"]))
            self.media_data["title"] = self.media_data["name"]
            self.media_data["release_date"] = self.media_data["first_air_date"]
            self.media_data["imdb_id"] = None


    def added(self):
        self.media_data = None
        self.movie_id_to_add = None
