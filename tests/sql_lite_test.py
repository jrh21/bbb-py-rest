#!flask/bin/python

# rest server


from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


users = contacts.query.all()
print(users)
# http messages
http_error = 404
http_success = 201


def __init__(self, username, email):
    self.username = username
    self.email = email


def serialize(self):
    return {"id": self.id, "name": self.username, 'email': self.username}


## index page
@app.route('/', methods=['GET'])
def index_page(io_num=None, val=None):
    return jsonify({'1_state': "whats up"}), http_success


@app.route('/dev/', methods=['GET'])
def index():
    return jsonify({'developers': list(map(lambda d: contacts.serialize(), contacts.query.all()))})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
