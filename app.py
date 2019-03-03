from flask import Flask, render_template ,session, escape, request, Response
from flask import url_for, redirect, send_from_directory
from flask import send_file, make_response, abort, jsonify
from flask import Flask, jsonify, request
import json
import os, sys

import pymongo
from pymongo import MongoClient

MONGO_PORT = 25058
MONGO_DB = "mtee"
MONGO_USER = "Admin1"
MONGO_PASS = "admin1"
MONGO_HOST = "mongodb://"+MONGO_USER+":"+MONGO_PASS+"MONGO_PATH"
connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
mongo = connection[MONGO_DB]

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

app = Flask(__name__)
app.secret_key="secret"

app.url_map.strict_slashes = False

@app.route('/')
def basic_pages(**kwargs):
    return make_response(open('checking.html').read())

@app.route('/home')
def basic_pages_login(**kwargs):
    return make_response(open('index.html').read())

#Register user
@app.route('/register', methods=['POST'])
def getAllRegions():
	name = request.json['name']
	question = request.json['question']
	answer = request.json['answer']
	main = request.json['main']
	helloRem = request.json['helloRem']
	helloAdd = request.json['helloAdd']
	howRem = request.json['howRem']
	howAdd = request.json['howAdd']
	insColor = {}
	color = []
	insColor['question'] = question
	insColor['answer'] = answer
	insColor['main'] = main
	color.append(insColor)
	hello = {}
	how = {}
	classData = []
	hello['remove'] = helloRem
	hello['add'] = helloAdd
	how['remove'] = howRem
	how['add'] = howAdd
	insClass = {}
	insClass['hello'] = hello
	insClass['how'] = how
	classData.append(insClass)
	insData = {}
	insData['name'] = name
	insData['class'] = classData
	insData['color'] = color
	data = mongo.userPref
	data.insert(insData)
	return jsonify({"result":"success"}), 200, {'Content-Type': 'application/json'}

#Login post request to get css info
@app.route('/login', methods=['POST'])
def login():
	name = request.json['name']
	data = mongo.userPref
	userInfo = data.find_one({'name':name}, {'_id': False})
	return jsonify({"result":"success","data":userInfo})
	
if __name__ == "__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 5000)))