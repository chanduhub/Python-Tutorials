from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json
from sqlalchemy.inspection import inspect
from math import sqrt
from math import sin, cos, sqrt, atan2, radians

# API in FLask to serve user requests

#Configuration of SQLAlchemy database and the table
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'pharma_test.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Creating model to store the values obtained from the database and the field distance is added to obtain requirements of the use case.
class Pharmacies(db.Model):
	__tablename__ = 'Pharmacies'
	name = db.Column(db.String)
	address = db.Column(db.String(120),primary_key=True)
	city = db.Column(db.String(20))
	state = db.Column(db.String(20))
	zip = db.Column(db.Integer)
	latitude = db.Column(db.Float)
	longitude = db.Column(db.Float)
	distance = 'value_1'
	
	def __init__(self, name, address, city, state, zip, latitude, longitude):
		self.name = name
		self.address = address
		self.city = city
		self.state = state
		self.zip = zip
		self.latitude = latitude
		self.longitude = longitude
		
		
	def __repr__(self):
		return self.name

	def apend(self, value):
		self.distance = value
		return self.distance


class PharmaSchema(ma.Schema):
	class Meta:
		# Fields to expose
		fields = ('name', 'address', 'city', 'state', 'zip', 'latitude', 'longitude', 'distance')


pharma_schema = PharmaSchema(only=('name','address', 'distance'))
pharmas_schema = PharmaSchema(many=True)


# endpoint to show all Pharmas
@app.route("/Pharma", methods=["GET"])
def get_pharma():
	all_Pharmas = Pharmacies.query.all()
	result = pharmas_schema.dump(all_Pharmas)
	return jsonify(result.data)


# endpoint to get Pharma detail by id
@app.route("/Pharma/<lat>/<lon>", methods=["GET"])
def Pharma_detail(lat,lon):
	print(lat,lon)
	#print(float(id))
	result = Pharmacies.query.filter(Pharmacies.latitude<=float(lat))\
	                         .filter(Pharmacies.longitude<=float(lon)).limit(1)
	print(type(lat))
	print(type(str(result[0].latitude)))
	x1 = float(lat)
	y1 = float(lon)
	
	
	# approximate radius of earth in km
	R = 6373.0

	lat1 = radians(x1)
	lon1 = radians(y1)
	print(str(result[0].latitude))
	lat2 = radians(float(str(result[0].latitude)))
	lon2 = radians(float(str(result[0].longitude)))

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	dist = R * c

	
	
	dummy = result[0]
	print(dummy)
	result[0].apend(dist)
	print(dummy.distance)
	dummy1 = [dummy]
	
	#return json.dumps(Pharmacies.serialize(result))
	#print(type(json(pharma_schema.jsonify(result,many=True))))
	return pharma_schema.jsonify(dummy1,many=True)
	
	

	


if __name__ == '__main__':
	app.run(debug=True)