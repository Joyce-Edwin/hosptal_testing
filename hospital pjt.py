from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
"""
@app.route('/', methods=['GET'])
def home():
    return jsonify({'name': 'joyce', 'message': 'welcome'})
    """
BASE_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_dir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init DB(object creation)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(150), unique=True)

    def __init__(self, name, contact):
        self.name = name
        self.contact = contact


class userschema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'contact')


user_schema = userschema()
users_schema = userschema(many=True)


# add new patient
@app.route('/patient', methods=['POST'])
def add_patient():
    name = request.json['name']
    contact = request.json['contact']
    new_patient = Patient(name, contact)
    db.session.add(new_patient)
    db.session.commit()
    return user_schema.jsonify(new_patient)


@app.route('/patient', methods=['GET'])
def get_details():
    patient_details = Patient.query.all()
    result = users_schema.dump(patient_details)
    return jsonify(result)


# show patient using id
@app.route('/patient/<id>', methods=['GET'])
def getBy_id(id):
    result1 = Patient.query.get(id)
    return user_schema.jsonify(result1)


# updatepatient using id
@app.route('/patient/<id>', methods=['PUT'])
def updateBy_id(id):
    result2 = Patient.query.get(id)
    name = request.json['name']
    contact = request.json['contact']
    result2.name = name
    result2.contact = contact
    db.session.commit()
    return user_schema.jsonify(result2)


@app.route('/patient/<id>', methods=['DELETE'])
def deleteBy_id(id):
    result4 = Patient.query.get(id)
    db.session.delete(result4)
    db.session.commit()
    return user_schema.jsonify(result4)


# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
