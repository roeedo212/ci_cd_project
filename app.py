from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import mysql.connector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:a1a1a1@localhost/recommended_films'
db = SQLAlchemy(app)

class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rate = db.Column(db.Integer, nullable=False)

@app.route('/movies/<int:year>')
def most_rated_films(year):
    result = get_most_rated_films(year)
    return render_template('movies.html', year=year, movies=result)

def get_most_rated_films(year):
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='a1a1a1',
        database='recommended_films'
    )
    cursor = conn.cursor()

    # Fetch movies with a rating of 4 and above for the given year
    query = '''
        SELECT name, rate FROM films WHERE year = %s AND rate >= 4 ORDER BY rate DESC
    '''
    cursor.execute(query, (year,))
    movies = cursor.fetchall()

    # Close the connection
    conn.close()

    return movies

if __name__ == '__main__':
    # Create the database schema
    db.create_all()

    app.run(host='0.0.0.0', port=5000)
