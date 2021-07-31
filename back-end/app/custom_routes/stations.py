from flask import Blueprint, request,current_app,Response
import datetime
import jwt
import re
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from db import *
from functions.conversions import *

stations = Blueprint('stations', __name__)



@stations.route("/")
def getAllStations():
    mycursor.execute("SELECT * FROM stations LIMIT 3000;")
    data = queryResToString(mycursor)
    return data

@stations.route("/points/<station_id>")
def getPointsPerStations(station_id):
    query = f"SELECT * FROM points,connectors where  points.station_id = '{station_id}'  and connectors.uuid = points.connection_uuid;"
    mycursor.execute(query)
    data = queryResToString(mycursor)         
    return data 

@stations.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Content-Type'] = 'application/json'
    if 'format' not in request.args: return response
    if request.args['format'] == 'csv':
        response.headers['Content-Type'] = 'text/csv'
        d = json.loads(response.get_data())
        # d['altered'] = 'this has been altered...GOOD!'
        new_res = checkIfNested(d)
        response.set_data(new_res)
        # response.set_data(json.dumps(d))
    return response

