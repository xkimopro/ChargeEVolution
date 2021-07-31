from flask import Blueprint, request,current_app,Response
import datetime
import jwt
import re
import sys
import os
import json
import pandas
sys.path.append(os.path.dirname(__file__))

# from db import *

import mysql.connector

from functions.conversions import *
from functions.connectionFunctions import *

admin = Blueprint('admin', __name__)

@admin.before_request
def auth_middleware():
    if not request.endpoint == "admin.checkHealth":
        jwt_token = request.headers.get('charge_evolution_token') 
        if not jwt_token: return {"status": 401, "msg": "No token "} 
        
        try:
            #  If token is valid check if user is admin
            payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
            if not payload['admin'] : return {"status": 401, "msg": "Not authorized "} 
            con = openConnection()
            if isinstance(con, dict):
                return con
            [mycursor,mydb] = con
            # Then check if token is blacklisted
            mycursor.execute( "SELECT * FROM token_blacklist WHERE token= %s ", (jwt_token, ) ) 
            if mycursor.rowcount == 1:
                return {"status": 401, "msg": "Token expired. Login again"}
            closeConnection(mydb,mycursor)
        except jwt.ExpiredSignatureError:
            return {"status": 400, "msg": "Expired token "}
        except jwt.InvalidTokenError:
            return {"status": 400, "msg": "Invalid token "}
        

@admin.route("/users")
def getAllUsers():
    [mycursor, mydb] = openConnection()
    mycursor.execute("SELECT * FROM users")
    data = queryResToString(mycursor)
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
        return data


@admin.route("/users/<username>")
def getUser(username):
    [mycursor, mydb] = openConnection()
    mycursor.execute( f"SELECT * FROM users WHERE username='{username}'" )           
    data = queryToDictList(mycursor)
    if data == '[]': 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "User not found."}
    else: 
        closeConnection(mydb,mycursor)
        return data[0]


@admin.route("/usermod/<username>/<password>", methods = ['POST'])
def modUser(username,password):
    fields = ["first_name","last_name", "telephone_number","email" ]
    
    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    
    # Check for every field needed 
    data = request.json
    for f in fields:
        if  f not in data:
            return {"status": 400, "msg": "Invalid request for field " + f}
    [mycursor, mydb] = openConnection()
    # Execute query
    mycursor.execute("SELECT * FROM users where username = %s", (username,))
    if mycursor.rowcount == 0:
        mycursor.execute( "INSERT IGNORE INTO users (first_name, last_name, telephone_number, email, username, password_hash) VALUES ( %s,%s,%s,%s,%s, MD5(%s) ) ON DUPLICATE KEY UPDATE password_hash = MD5(%s) " ,(data['first_name'],data['last_name'],data['telephone_number'],data['email'],username,password, password) ) 
    else:
        mycursor.execute("UPDATE users set password_hash = MD5(%s) WHERE username = %s", (password,username))
    # mycursor.execute("INSERT IGNORE INTO user_wallets (user_id, wallet) VALUES (LAST_INSERT_ID(), 0)")
    mydb.commit()
    # Return results
    if mycursor.rowcount == 0: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "SQL failed! Same password or invalid username/password length "}   
    else: 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Modified successfully "}



@admin.route("/system/resetsessions")
def resetSessions():
    [mycursor, mydb] = openConnection()
    mycursor.execute("TRUNCATE TABLE sessions")    
    mycursor.execute("UPDATE admin SET password_hash = MD5('123') WHERE username = 'admin'")    
    mydb.commit()
    if mycursor.rowcount == 0: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "SQL failed! could not reset sessions "}   
    else:
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Reset successful"}



@admin.route("/system/sessionsupd")
def sessionsUpload():
    file = request.files['file']
    df = pandas.read_csv(file,header=None, names=["session_id","user_id","point_id","station_id","transaction_id","plate_number","cost_per_kwh","connection_time","disconnection_time","kwh_delivered","fast_charging"])  
    insert_prefix = "INSERT INTO sessions (session_id, user_id, point_id, station_id, transaction_id, plate_number, cost_per_kwh, connection_time, disconnection_time, kwh_delivered, fast_charging) VALUES "
    for x in df.to_dict('records'):
        values_str = f"('{x['session_id']}',{x['user_id']},{x['point_id']},'{x['station_id']}','{x['transaction_id']}','{x['plate_number']}',{x['cost_per_kwh']},'{x['connection_time']}','{x['disconnection_time']}',{x['kwh_delivered']},{x['fast_charging']}),"
        insert_prefix += values_str
        print(values_str)
    insert_prefix = insert_prefix[:-1]
    [mycursor, mydb] = openConnection()
    mycursor.execute(insert_prefix)
    mydb.commit()
    if mycursor.rowcount == 0: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "SQL failed! could not upload "}   
    else: 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Files uploaded"}


    
@admin.route("/system/newstation", methods = ['POST'])
def stationUpload():
    file = request.files['file']
    df = pandas.read_csv(file,header=None, names=["station_id","station_name","operator_id","postcode","latitude","longitude","address","town","country","email","phone", "provider_id"])  
    insert_prefix = """      INSERT INTO sessions (station_id, station_name, operator_id, postcode, latitude, longitude, address, town, country, email, phone, provider_id) VALUES """
    for x in df.to_dict('records'):
        values_str =   f"('{x['station_id']}',{x['station_name']},{x['operator_id']},'{x['postcode']}','{x['latitude']}','{x['longitude']}',{x['address']},'{x['town']}','{x['country']}',{x['email']},{x['phone']},{x['provider_id']}),"
        insert_prefix += values_str
        print(values_str)
    insert_prefix = insert_prefix[:-1]
    [mycursor, mydb] = openConnection()
    mycursor.execute(insert_prefix)
    mydb.commit()
    if mycursor.rowcount == 0: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "SQL failed! could not upload "}   
    else: 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Files uploaded. New stations added"}
    
@admin.route("/system/deletestation/<station_id>", methods = ['POST'])
def stationDel(station_id):   
    [mycursor, mydb] = openConnection()
    mycursor.execute(f"DELETE FROM stations WHERE station_id = '{station_id}'")
    mydb.commit()
    if mycursor.rowcount == 0: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "SQL failed! Could not delete. Maybe the station you want to delete doesn't exit in the DB or has been already deleted."}   
    else: 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": f"Station with id:{station_id} deleted"}
    
    
@admin.route("/healthcheck")
def checkHealth():
    try :
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="chargeevolution"
        )        
        return {"status" : "OK"}
    except Exception as e:
        return {"status" : "Failed"}


@admin.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response

