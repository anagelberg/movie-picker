$env:SECRET_KEY="YOUR_SECRET_KEY";
$env:TMDB_API_KEY="TMDB_API_KEY";
cd C:/path/to/movie-picker;
waitress-serve --host 127.0.0.1 main:app