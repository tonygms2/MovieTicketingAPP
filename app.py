from datetime import datetime,timedelta
import os
from random import randint
from flask import Flask, jsonify,request
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import mysql.connector
import requests
# from dotenv import load_dotenv
#
# load_dotenv()


app = Flask(__name__)
CORS(app)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movie_ticketing'

mysql = MySQL(app)

bcrypt = Bcrypt(app)
#region populate DB
# OMDB_API_KEY = 'f2e94d5b'
#
# movies_list = [
#     'The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction',
#     'Schindler\'s List', 'The Lord of the Rings: The Return of the King', 'Fight Club',
#     'Forrest Gump', 'Inception', 'The Matrix', 'Goodfellas', 'The Empire Strikes Back',
#     'The Silence of the Lambs', 'Saving Private Ryan', 'The Green Mile', 'Interstellar',
#     'Parasite', 'Gladiator', 'The Departed', 'The Prestige', 'Scarface', 'Paglu 2','The Big Bang Theory'
# ]
#
# @app.route('/fetch_movies', methods=['GET'])
# def fetch_movies():
#     cursor = mysql.connection.cursor()
#
#     for movie in movies_list:
#         url = f'http://www.omdbapi.com/?t={movie}&apikey={OMDB_API_KEY}'
#         response = requests.get(url)
#         data = response.json()
#         if data['Response'] == 'True':
#             title = data.get('Title')
#             genre = data.get('Genre')
#             director = data.get('Director')
#             release_year = data.get('Year')
#             imdb_rating = data.get('imdbRating')
#             poster_url = data.get('Poster')
#             duration = data.get('Runtime')
#             description = data.get('Plot')
#             cursor.execute("""
#                 INSERT INTO movies (title, genre, director, release_year, imdb_rating, poster_url, duration, description)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
#                 ON DUPLICATE KEY UPDATE
#                 genre=VALUES(genre), director=VALUES(director), release_year=VALUES(release_year),
#                 imdb_rating=VALUES(imdb_rating), poster_url=VALUES(poster_url), duration=VALUES(duration), description=VALUES(description)
#             """, (title, genre, director, release_year, imdb_rating, poster_url, duration, description))
#
#     mysql.connection.commit()
#     cursor.close()
#
#     return jsonify({"message": "Movies data inserted/updated successfully!"})
#endregion

#region API ROUTES
#route to fetch list of movies from the DB
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
            'id': row[0],
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


@app.route('/showtimes/<int:movie_id>', methods=['GET'])
def get_showtimes(movie_id):
    cursor = None
    try:
        cursor = mysql.connection.cursor()

        # First, check if the movie exists
        cursor.execute('SELECT title FROM movies WHERE id = %s', (movie_id,))
        movie = cursor.fetchone()
        if not movie:
            return jsonify({"error": "Movie not found"}), 404

        # Fetch showtimes
        cursor.execute('SELECT id, movie_id, showtime FROM showtimes WHERE movie_id = %s', (movie_id,))
        showtimes = cursor.fetchall()

        showtimes_list = []
        for showtime in showtimes:
            showtimes_list.append({
                "id": showtime[0],
                "movie_id": showtime[1],
                "showtime": showtime[2].strftime("%Y-%m-%d %H:%M:%S") if isinstance(showtime[2], datetime) else str(
                    showtime[2])
            })

        return jsonify({
            "movie_title": movie[0],
            "showtimes": showtimes_list
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
@app.route('/book', methods=['POST'])
def book_tickets():
    data = request.get_json()
    showtime_id = data['showtime_id']
    user_id = data['user_id']
    seats = data['seats']
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO bookings (showtime_id,user_id,seats) VALUES (%s,%s,%s)",
                   (showtime_id,user_id,seats))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': "Your booking has been successfully submitted!"})


#Seat selection route
@app.route('/seats/<int:showtime_id>', methods=['GET'])
def get_seats(showtime_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM seats WHERE show_id = %s", (showtime_id,))
    seats = cursor.fetchall()
    cursor.close()

    seats_list = []
    for seat in seats:
        seats_list.append({
            "id": seat[0],
            "showtime_id": seat[1],
            "seat_number": seat[2],
            "is_booked": seat[3]
        })

    return jsonify(seats_list)


#registration




@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    mobile_number = data['mobile_number']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    cursor = mysql.connection.cursor()
    try:
        cursor.execute("""
            INSERT INTO users (username, password, mobile_number)
            VALUES (%s, %s, %s)
        """, (username, hashed_password, mobile_number))
        mysql.connection.commit()
    except mysql.connector.IntegrityError:
        return jsonify({"message": "Username already exists."}), 400

    cursor.close()
    return jsonify({"message": "User registered successfully!"})




@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if user and bcrypt.check_password_hash(user[2], password):
        return jsonify({
            "user_id": user[0],
            "message": "Login successful!",
            "isLoginSuccess": True  # Directly return True for success
        })
    else:
        return jsonify({
            "message": "Invalid username or password.",
            "isLoginSuccess": False
        }), 401


# @app.route('/generate_showtimes', methods=['GET'])
# def generate_showtimes():
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT id FROM movies')
#     movie_ids = cursor.fetchall()
#
#     now = datetime.now()
#
#     for movie_id in movie_ids:
#         movie_id = movie_id[0]
#         for _ in range(5):  # Generate 5 showtimes per movie
#             showtime = now + timedelta(days=randint(0, 7), hours=randint(8, 23))
#             cursor.execute("""
#                 INSERT INTO showtimes (movie_id, showtime)
#                 VALUES (%s, %s)
#             """, (movie_id, showtime))
#             mysql.connection.commit()
#
#     cursor.close()
#     return jsonify({"message": "Showtimes generated successfully!"})

#endregion

if __name__ == '__main__':
    app.run(debug=True)
