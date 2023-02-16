from flask import Flask
import random
app = Flask(__name__)

the_number = 5


def center(function):
    def wrapper():
        func = function()
        return f"<div style='text-align:center'>{func}</div>"
    return wrapper


@app.route("/")
@center
def game_start():
    global the_number
    the_number = random.randint(0, 9)
    print(f"The random number is {the_number}")
    return '<h1>Guess a number between 1 and 10</h1>' \
           '<img src="https://media.giphy.com/media/NAy2FD8xWrH4jUIBrq/giphy-downsized-large.gif">'


@app.route("/<int:guess>")
def guess_a_number(guess):
    if guess == the_number:
        return("<h1 style='color:red'>You win!</h1>"
               "<img src='https://media.giphy.com/media/fXLHAkIvVuggw/giphy.gif'>")
    elif the_number > guess:
        return("<h1 style='color:red'>Too Low</h1>"
               "<img src='https://media.giphy.com/media/2uI9astifwiSUWVOTT/giphy.gif'>")
    elif the_number < guess:
        return("<h1 style='color:red'>Too High</h1>"
               "<img src='https://media.giphy.com/media/79eQOjPPrisR9B2zy6/giphy.gif'>")


if __name__ == "__main__":
    app.run(debug=True)
