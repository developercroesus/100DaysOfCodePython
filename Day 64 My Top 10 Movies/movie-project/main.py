from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import os

TMDB_KEY = os.environ.get('TMDB_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = "This is the big secret"
Bootstrap(app)

# create the extension
# create the app
# configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///movie-list.db"
# initialize the app with the extension
db = SQLAlchemy()
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(250), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_url = db.Column(db.String,)

    def __repr__(self):
        return f"{self.title} rating: {self.rating} rank: {self.ranking}"


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    top_movies = db.session.query(Movie).all()
    top_movies.sort(key=lambda x: x.rating)
    rank = len(top_movies)
    for movie in top_movies:
        Movie.query.get(movie.id).ranking = rank
        rank -= 1
    db.session.commit()
    return render_template('index.html', movies=top_movies)


class RateMovieForm(FlaskForm):
    rating = StringField('Your rating out of 10 e.g. 7.5', validators=[DataRequired()])
    review = StringField('Your review:', validators=[DataRequired()])
    submit = SubmitField('Done')


@app.route("/edit", methods=['GET', 'POST'])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get("id")
    movie_to_edit = Movie.query.get(movie_id)
    if form.validate_on_submit():
        # Make changes to db
        movie_to_edit.rating = float(form.rating.data)
        movie_to_edit.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie_to_edit)


@app.route("/delete")
def delete_movie():
    movie_id = request.args.get("id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


class AddMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    submit = SubmitField('Add Movie')


@app.route("/add", methods=['GET', 'POST'])
def select_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie = form.title.data
        headers = {'Accept': 'application/json'}
        url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_KEY}&language=en-US' \
              f'&query={movie}&page=1&include_adult=false'
        response = requests.get(url, headers=headers)
        results = response.json()['results']
        return render_template('select.html', movie_list=results)
    return render_template('add.html', form=form)


@app.route("/update/<int:movie_id>")
def add_movie_to_db(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_KEY}"
    response = requests.get(url)
    data = response.json()
    title = data['title']
    img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    year = int(data['release_date'].split("-")[0])
    description = data['overview']
    new_movie = Movie(title=title, img_url=img_url, year=year, description=description)
    db.session.add(new_movie)
    db.session.commit()
    movie = Movie.query.filter_by(title=title).first()
    return redirect(url_for('rate_movie', id=movie.id))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
