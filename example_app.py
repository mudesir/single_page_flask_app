"""Example of a one file Flask application that uses API and Alchemy"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
DB = SQLAlchemy(app)


@app.route("/")
def root():
    astro_data = Astronauts.query.all()
    return "There are {} astronauts in space right now!".format(astro_data[0].num_astros)


@app.route("/refresh")
def refresh():
    # Reset DB
    DB.drop_all()
    DB.create_all()
    # Grab data from endpoint
    request = requests.get("http://api.open-notify.org/astros.json")
    astro_data = request.json()
    num_astros = astro_data["number"]
    # Save to DB
    record = Astronauts(num_astros=num_astros)
    DB.session.add(record)
    DB.session.commit()
    return "The astros have been updated!"


# Astronaut table in sqlite DB - SQLAlchemy
class Astronauts(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astros = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        return "# of Astros in space: {}".format(self.num_astros)
