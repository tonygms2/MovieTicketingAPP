from flask import Flask,request,jsonify,render_template
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'movie_ticketing'

mysql = MySQL(app)

@app.route('/movies', methods=['GET'])
def get_movies():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    cursor.close()
    return jsonify(movies)



if __name__ == '__main__':
    app.run(debug=True)


