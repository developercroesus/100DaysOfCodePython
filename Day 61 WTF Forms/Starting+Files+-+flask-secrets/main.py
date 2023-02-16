from flask import Flask, render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap


class MyForm(FlaskForm):
    email = EmailField(label='Email',
                       validators=[DataRequired(), Email(granular_message=True,check_deliverability=True)])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label='Log In')


def create_app():
    app = Flask(__name__)
    app.secret_key = "This is my very secret key"
    Bootstrap(app)

    return app


app = create_app()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    login_form = MyForm()

    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com":
            if login_form.password.data == "12345678":
                return render_template('success.html')

    if login_form.validate_on_submit():
        return render_template('denied.html')
    return render_template('login.html', form=login_form)



@app.route("/quick-form", methods=['GET', 'POST'])
def quick():
    login_form = MyForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com":
            if login_form.password.data == "12345678":
                return render_template('success.html')

    if login_form.validate_on_submit():
        return render_template('denied.html')
    return render_template('quick-form.html', form=login_form)




if __name__ == '__main__':
    app.run(debug=True)
