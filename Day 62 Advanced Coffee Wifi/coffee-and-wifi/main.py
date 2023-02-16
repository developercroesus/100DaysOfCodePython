from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a very secret key'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    url = URLField(label='Map Link', validators=[URL()])
    opening_time = StringField(label='Opening time e.g. 8AM')
    closing_time = StringField(label='Closing Time e.g. 5:30PM')
    coffee_rating = SelectField(label='Coffee Rating',
                                choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️', '✘'])
    wifi_strength = SelectField(label='Wifi Strength Rating',
                                choices=['💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪', '✘'])
    power_sockets = SelectField(label='Power Socket Availability',
                                choices=['🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌', '✘'])

    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, Wi-Fi rating, power outlet rating fields
# make coffee/Wi-Fi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
        with open('cafe-data.csv', 'a', encoding="utf8") as csv_file:
            data = f"{form.cafe.data},{form.url.data},{form.opening_time.data},{form.closing_time.data}," \
                   f"{form.coffee_rating.data},{form.wifi_strength.data},{form.power_sockets.data}\n"
            csv_file.write(data)
            print(data)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
