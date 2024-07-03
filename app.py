import os

from flask import Flask, jsonify
from flask_mysqldb import MySQL
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movie_ticketing'

mysql = MySQL(app)

# OMDb API key
OMDB_API_KEY = os.getenv('OMDB_API_KEY')

print(OMDB_API_KEY)

movies_list = [
    'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction',
    'Schindler\'s List', 'The Lord of the Rings: The Return of the King', 'Fight Club',
    'Forrest Gump', 'Inception', 'The Matrix', 'Goodfellas', 'The Empire Strikes Back',
    'The Silence of the Lambs', 'Saving Private Ryan', 'The Green Mile', 'Interstellar',
    'Parasite', 'Gladiator', 'The Departed', 'The Prestige'
]


@app.route('/fetch_movies', methods=['GET'])
def fetch_movies():
    cursor = mysql.connection.cursor()

    for movie in movies_list:
        url = f'http://www.omdbapi.com/?t={movie}&apikey={OMDB_API_KEY}'
        response = requests.get(url)
        data = response.json()
        if data['Response'] == 'True':
            title = data.get('Title')
            genre = data.get('Genre')
            director = data.get('Director')
            release_year = data.get('Year')
            imdb_rating = data.get('imdbRating')
            poster_url = data.get('Poster')
            duration = data.get('Runtime')

            cursor.execute("""
                INSERT INTO movies (title, genre, director, release_year, imdb_rating, poster_url, duration)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                genre=VALUES(genre), director=VALUES(director), release_year=VALUES(release_year),
                imdb_rating=VALUES(imdb_rating), poster_url=VALUES(poster_url), duration=VALUES(duration)
            """, (title, genre, director, release_year, imdb_rating, poster_url, duration))

    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Movies data inserted/updated successfully!"})


@app.route('/movies', methods=['GET'])
def get_movies():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM movies')
    rows = cursor.fetchall()
    cursor.close()

    movies = []
    for row in rows:
        print(row)
        movie = {
            'title': row[1],
            'genre': row[2],
            'director': row[8],
            'release_year': row[4],
            'imdb_rating': row[5],
            'poster_url': row[6],
            'duration': row[7]
        }
        movies.append(movie)

    return jsonify(movies)


@app.route('/shows', methods=['GET'])
def get_shows():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM showtimes')
    rows = cursor.fetchall()
    cursor.close()

    # Map each row to the desired JSON structure
    shows = []
    for row in rows:
        show = {
            'id': row[0],
            'movie_id': row[1],
            'showtime': row[2].strftime('%Y-%m-%d %H:%M:%S')
        }
        shows.append(show)

    return jsonify(shows)


if __name__ == '__main__':
    app.run(debug=True)
