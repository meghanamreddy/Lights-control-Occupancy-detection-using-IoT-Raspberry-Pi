#september 20 2016
#web server code. runs a web app to collect occupancy data. 
#user has to manually click on the button while leaving or entering the room.
#whenever a person enters or leaves the room, data is saved.

import time
import random
import sys
import datetime
from flask import Flask
from flask import json, render_template, jsonify
from pymongo import MongoClient


client = MongoClient('mongodb://username:password@ds141410.mlab.com:41410/meghana_pe')

#webapp code
app = Flask(__name__)

# "person01" : 1 - in.. 0 - out.

@app.route("/")
def render():
        return render_template('occupancy.html')

@app.route("/person1_toggle_true")
def person1_toggle_in():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person01":"1"})
	return jsonify({"hi":"hello"})

@app.route("/person1_toggle_false")
def person1_toggle_out():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person01":"0"})
	return jsonify({"hi":"hello"})


@app.route("/person2_toggle_true")
def person2_toggle_in():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person02":"1"})
	return jsonify({"hi":"hello"})

@app.route("/person2_toggle_false")
def person2_toggle_out():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person02":"0"})
	return jsonify({"hi":"hello"})

@app.route("/person3_toggle_true")
def person3_toggle_in():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person03":"1"})
	return jsonify({"hi":"hello"})

@app.route("/person3_toggle_false")
def person3_toggle_out():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person03":"0"})
	return jsonify({"hi":"hello"})

@app.route("/person4_toggle_true")
def person4_toggle_in():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person04":"1"})
	return jsonify({"hi":"hello"})

@app.route("/person4_toggle_false")
def person4_toggle_out():
	db = client.meghana_pe
	collection = db.rfid2
	loc_time = str(datetime.datetime.now())
	collection.insert_one({"timestamp":loc_time, "person04":"0"})
	return jsonify({"hi":"hello"})


#webapp code end

if __name__=="__main__":
	try:	
		app.run(host='0.0.0.0')
	finally:
		sys.exit()
