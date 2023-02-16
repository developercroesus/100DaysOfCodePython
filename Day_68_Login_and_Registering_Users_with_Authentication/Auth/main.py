from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = str(os.environ.get('SECRET'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name

    def get_id(self):
        return str(self.email)


# Line below only required once, when creating DB.
# with app.app_context():
#     db.create_all()


@login_manager.user_loader
def load_user(user_id):
    email = user_id
    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
    return user


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user_email = request.form.get('email')
        if user_email in all_email_list():
            flash("An account with this email already exists")
            return render_template("register.html")
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=user_email,
            name=request.form.get('name'),
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        user = load_user(user_email)
        login_user(user)
        return redirect(url_for('secrets'))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email in all_email_list():
            user_to_check = db.session.execute(db.select(User).filter_by(email=email)).scalar_one()
            if check_password_hash(password=password, pwhash=user_to_check.password):
                login_user(load_user(email))
                flash('You were successfully logged in')
                return redirect(url_for("secrets"))
            else:
                flash("Wrong password!")
        else:
            flash("Email account does not exist")
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.name)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory(directory=app.static_folder, path='files/cheat_sheet.pdf')


def all_email_list():
    all_users = db.session.query(User).all()
    the_list = [user.email for user in all_users]
    return the_list


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
