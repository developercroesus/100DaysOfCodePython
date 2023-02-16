import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"{self.name}"

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

        # Method 2. Alternatively use Dictionary Comprehension to do the same thing.
        # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=['PATCH'])
def update_price(cafe_id):
    new_price = request.args.get('new_price')
    cafe_to_update = db.session.get(Cafe, cafe_id)
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        # Just add the code after the jsonify method. 200 = Ok
        return jsonify(response={"success": "Successfully updated the price."}), 200
    else:
        # 404 = Resource not found
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=['DELETE'])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Auth": "Sorry, that's not allowed. Make sure you have the correct api_key"}), 403


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random")
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    # random_cafe_dict = {
    #     "cafe": {
    #         "can_take_calls": random_cafe.can_take_calls,
    #         "coffee_price": random_cafe.coffee_price,
    #         "has_sockets": random_cafe.has_sockets,
    #         "has_toilet": random_cafe.has_toilet,
    #         "has_wifi": random_cafe.has_wifi,
    #         "id": random_cafe.id,
    #         "img_url": random_cafe.img_url,
    #         "location": random_cafe.location,
    #         "map_url": random_cafe.map_url,
    #         "name": random_cafe.name,
    #         "seats": random_cafe.seats,
    #     }
    # }
    # cafe_dictionary = dict(random_cafe.__dict__)
    # del cafe_dictionary["_sa_instance_state"]
    return jsonify(cafe=random_cafe.to_dict())

    # return jsonify(random_cafe_dict)
    # return render_template("random.html", cafe=random_cafe)


@app.route("/all")
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    # cafes_dict = []
    # for café in cafes:
    #     cafes_dict.append(cafe.to_dict())
    # return jsonify(cafes=cafes_dict)
    # Here is a good example of a list comprehension replacing a loop.
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])


@app.route("/add", methods=['POST'])
def add_cafe():
    name = request.form['name']
    map_url = request.form['map_url']
    seats = request.form['seats']
    location = request.form['location']
    img_url = request.form['img_url']
    has_toilet = request.form['has_toilet'] == 'true'
    has_wifi = request.form['has_wifi'] == 'true'
    has_sockets = request.form['has_sockets'] == 'true'
    can_take_calls = request.form['can_take_calls'] == 'true'
    coffee_price = request.form['coffee_price']
    new_cafe = Cafe(name=name,
                    map_url=map_url,
                    seats=seats,
                    location=location,
                    has_wifi=has_wifi,
                    img_url=img_url,
                    has_toilet=has_toilet,
                    has_sockets=has_sockets,
                    can_take_calls=can_take_calls,
                    coffee_price=coffee_price)

    db.session.add(new_cafe)
    db.session.commit()
    return {
                "response": {
                    "success": "Successfully added the new cafe.",
                    "name": name,
                    "map_url": map_url,
                    "seats": seats
                }
            }


@app.route("/search")
def search():
    cafes = db.session.query(Cafe).all()
    location_to_find = request.args.get("loc")
    locations = [cafe.to_dict() for cafe in cafes if cafe.location == location_to_find]
    if locations:
        return jsonify(locations)
    else:
        return {"error": {"Not Found": "Sorry, we don't have a cafe at that location."}}
    # cafes = db.session.query(Cafe).all()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
