from flask import Flask

app = Flask(__name__)


def make_bold(function):
    def wrapper():
        func = function()
        return f"<b>{func}</b>"
    return wrapper


def make_emphasis(function):
    def wrapper():
        func = function()
        return f"<em>{func}</em>"
    return wrapper


def make_underlined(function):
    def wrapper():
        func = function()
        return f"<u>{func}</u>"
    return wrapper


@app.route('/')
def hello_world():
    return '<h1 style="text-align:center">Hello, Cruel World!</h1>' \
           '<p>This is a paragraph</p>' \
           '<img width=200 src="https://media.giphy.com/media/Puc4FZWExJc0E/giphy.gif">'


@app.route("/bye")
@make_bold
@make_emphasis
@make_underlined
def say_bye():
    return "Bye"


@app.route("/username/<name>/<int:number>")
def greet(name, number):
    return f"Hello there {name}, you are {number} years old!"


if __name__ == "__main__":
    app.run(debug=True)
