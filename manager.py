import os
import requests


class DbManager():
    def __init__(self):
        self.current_watchlist = None
        self.current_id_list = None
        self.movie_id_to_add = None
        self.all_genres = None
        self.all_watchlists = None

    def get_data(self, all_movies, all_watchlists):
        all_genres = []
        for movie in all_movies:
            for genre in movie.genre.split(","):
                all_genres.append(genre)
        self.all_genres = list(set(all_genres))
        self.all_watchlists = [list.name for list in all_watchlists]


class SearchManager():
    def __init__(self):
        self.title_results = None
        self.movie_data = None
        self.movie_id_to_add = None
        self.TMDB_API_KEY = os.environ['TMDB_API_KEY']

    def search_tmdb_titles(self, title):
        parameters = {
            'api_key': self.TMDB_API_KEY,
            'language': 'en-US',
            'query': title,
        }
        response = requests.get(url='https://api.themoviedb.org/3/search/movie', params=parameters)
        response.raise_for_status()
        data = response.json()
        self.title_results = data['results']

    def search_tmdb_details(self, tmdb_id):
        parameters = {
            'api_key': self.TMDB_API_KEY,
        }
        response = requests.get(url=f'https://api.themoviedb.org/3/movie/{tmdb_id}', params=parameters)
        response.raise_for_status()
        self.movie_data = response.json()

        if self.movie_data["poster_path"]:
            self.movie_data["poster_url"] = self.movie_data["poster_path"]
        elif self.movie_data['belongs_to_collection']:
            self.movie_data["poster_url"] = self.movie_data['belongs_to_collection']['poster_path']
        else:
            # TODO: make a placeholder?
            self.movie_data["poster_url"] = None

        genre_list = [genre["name"] for genre in self.movie_data["genres"]]
        self.movie_data["genre_string"] = ', '.join(genre_list)

    def added(self):
        self.movie_data = None
        self.movie_id_to_add = None
