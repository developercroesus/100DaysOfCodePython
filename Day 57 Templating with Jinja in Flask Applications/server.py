from flask import Flask, render_template
from random import randint
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    random_number = randint(1, 100)
    current_year = datetime.datetime.now().year
    return render_template("index.html", random_number=random_number, current_year=current_year)


@app.route('/guess/<name>')
def guess(name):
    response = requests.get(f"https://api.genderize.io?name={name}")
    gender = response.json()
    response2 = requests.get(f"https://api.agify.io?name={name}")
    age = response2.json()
    return render_template("guess.html", name=name.title(), gender=gender['gender'], age=age['age'])


@app.route('/blog')
def blog():
    url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(url)
    all_posts = response.json()
    print(all_posts)
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
