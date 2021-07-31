from flask import Blueprint,Response ,request,current_app
import jwt
import re
import sys
import os
import string
import random


sys.path.append(os.path.dirname(__file__))

# from db import *
import mysql.connector

from functions.conversions import *
from functions.timeseries import *
from functions.connectionFunctions import *

users = Blueprint('users', __name__)

@users.before_request
def auth_middleware():
    
    unprotected = {"users.registerUser","users.login","users.validateToken" }
    if  request.endpoint not in unprotected :
        jwt_token = request.headers.get('charge_evolution_token') 
        if not jwt_token: return {"status": 401, "msg": "No token "} 
        try:
            # Validate cookie
            payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
            # Then check if token is blacklisted
            con = openConnection()
            if isinstance(con, dict): return con
            [mycursor,mydb] = con
            mycursor.execute( "SELECT * FROM token_blacklist WHERE token= %s ", (jwt_token, ) ) 
            if mycursor.rowcount == 1:
                closeConnection(mydb,mycursor)
                return {"status": 401, "msg": "Token expired. Login again"}

        except jwt.ExpiredSignatureError:
            closeConnection(mydb,mycursor)
            return {"status": 400, "msg": "Expired token "}
        except jwt.InvalidTokenError:
            closeConnection(mydb,mycursor)
            return {"status": 400, "msg": "Invalid token "}






@users.route("/register", methods = ['POST'])
def registerUser():
    fields = ["first_name","last_name", "telephone_number","email","username","password" ]
    
    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    
    # Check for every field needed 
    data = request.json
    for f in fields:
        if f not in data:
            return {"status": 400, "msg": "Invalid request for field " + f}

    # Execute query
    [mycursor, mydb] = openConnection()
    mycursor.execute( """INSERT IGNORE INTO users (first_name, last_name, telephone_number, email, username, password_hash)
                         VALUES ( %s,%s,%s,%s,%s,MD5(%s) )""" ,(data['first_name'],data['last_name'],data['telephone_number'],data['email'],data['username'],data['password']) )  
    mycursor.execute("INSERT IGNORE INTO user_wallets (user_id, wallet) VALUES (LAST_INSERT_ID(), 0)")
    mydb.commit()
        
   
    # Return results
    if not mycursor.rowcount: 
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There is already a user with this email or username "}
    else:
        token = jwt.encode({'username': data['username'], 'admin': False ,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)}, current_app.config['SECRET_KEY'], algorithm="HS256") 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "User registered successfully" , "token": str(token)}


@users.route("/addVehicle/<user_id>", methods = ['POST'])
def addVehicle(user_id):
    fields = ["plate_number","vehicle_id"]
    
    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    
    # Check for every field needed 
    data = request.json
    for f in fields:
        if f not in data:
            return {"status": 400, "msg": "Invalid request for field " + f}

    # Execute query
    [mycursor, mydb] = openConnection()

    mycursor.execute( """SELECT * FROM vehicles WHERE id = %s """ ,(data['vehicle_id'],) )
    if mycursor.rowcount == 0:
        closeConnection(mydb,mycursor)
        return {"status": 400, "msg": "Invalid vehicle id "}

    res = queryToDictList(mycursor)[0]
    current_battery = 0.5 * res['usable_battery_size']
    current_battery_percentage = 50

    mycursor.execute( """INSERT IGNORE INTO user_vehicles (user_id, vehicle_id, plate_number, current_battery_percentage, current_battery)
                         VALUES ( %s,%s,%s,%s,%s )""" ,(user_id,data['vehicle_id'],data['plate_number'],current_battery_percentage,current_battery) )  
    mydb.commit()
        
    # Return results
    if mycursor.rowcount == 0:
        closeConnection(mydb,mycursor)
        return {"status": 400, "msg": "Could not insert vehicle "} 
    closeConnection(mydb,mycursor)
    return {"status": 200, "msg": "Vehicle added successfully"}   


@users.route("/login", methods = ['POST'])
def login():
    fields = ["username","password"]

    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    # Check for every field needed 
    data = request.json
    for f in fields:
        if f not in data:
            return {"status": 400, "msg": "Invalid request for field " + f}
    
    # SQL query for admin login first
    [mycursor, mydb] = openConnection()
    mycursor.execute( "SELECT * FROM admin WHERE username= %s and password_hash = MD5(%s)", (data['username'], data['password']) )
    # Admin with these credentials exists
    if mycursor.rowcount == 0: 
        # SQL query for user next
        mycursor.execute( "SELECT * FROM users WHERE username= %s and password_hash = MD5(%s)", (data['username'], data['password']) )
        if mycursor.rowcount == 0:
            return { 'status': 402 , 'msg': "No user or admin found" }
        
        row = queryToDictList(mycursor)[0]         
        token = jwt.encode({ 'id':row['id'] ,  'username': data['username'], 'admin': False ,'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=1440)}, current_app.config['SECRET_KEY'], algorithm="HS256")
    else:
        row = queryToDictList(mycursor)[0]   
        token = jwt.encode({ 'id':row['id'] , 'username':data['username'] , 'admin':True , 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=2880)}, current_app.config['SECRET_KEY'], algorithm="HS256")
    closeConnection(mydb,mycursor)
    return { "status":200 , "token":token }




@users.route("/logout", methods = ['POST'])
def logout():

    jwt_token = request.headers.get('charge_evolution_token') 

    try :
        payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
        # mydb = mysql.connector.connect( host="localhost", user="root", password="", database="chargeevolution")
        [mycursor, mydb] = openConnection()
        mycursor.execute("INSERT INTO token_blacklist ( token ) VALUES ( %s )" , (jwt_token,) )
        mydb.commit()
        if mycursor.rowcount == 0:
            closeConnection(mydb,mycursor)
            return {"status": 401, "msg": "Could not delete token "} 
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Logged out successfully"}
    except jwt.ExpiredSignatureError:
        closeConnection(mydb,mycursor)
        return {"status": 401, "msg": "Expired token "}
    except jwt.InvalidTokenError:
        closeConnection(mydb,mycursor)
        return {"status": 401, "msg": "Invalid token "}



@users.route("/validate", methods = ['POST'])
def validateToken():
    try:
        [mycursor, mydb] = openConnection()
        # Validate cookie
        jwt_token = request.headers.get('charge_evolution_token')
        payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
        # Then check if token is blacklisted
        mycursor.execute( "SELECT * FROM token_blacklist WHERE token= %s ", (jwt_token, ) ) 
        if mycursor.rowcount == 1:
            closeConnection(mydb,mycursor)
            return {"status": 401, "msg": "Token expired. Login again"}
        return {"status": 200, "msg": "Token Validated"}
    except jwt.ExpiredSignatureError:
        closeConnection(mydb,mycursor)
        return {"status": 401, "msg": "Expired token "}
    except jwt.InvalidTokenError:
        closeConnection(mydb,mycursor)
        return {"status": 401, "msg": "Invalid token "}


@users.route("/transactions/<user_id>/<date_from>/<date_to>")
def transactionsPerUser(user_id,date_from,date_to):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    [mycursor, mydb] = openConnection()
    mycursor.execute("SELECT * FROM transactions WHERE user_id = %s AND DATE(payment_timestamp) >= %s AND DATE(payment_timestamp) <= %s ", (user_id,date_from,date_to) )
    data = queryResToStringDateTimes(mycursor)
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return data

@users.route("/sessions/<user_id>/<date_from>/<date_to>")
def sessionsPerUser(user_id,date_from,date_to):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    [mycursor, mydb] = openConnection()
    mycursor.execute("SELECT * FROM sessions WHERE user_id = %s AND DATE(disconnection_time) >= %s AND DATE(disconnection_time) <= %s ", (user_id,date_from,date_to) )
    data = queryResToStringDateTimes(mycursor)
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return data


@users.route("/vehicles/<user_id>")
def viewVehicles(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    query = f"SELECT * FROM user_vehicles, vehicles where user_vehicles.user_id = {user_id} and user_vehicles.vehicle_id = vehicles.id"
    [mycursor, mydb] = openConnection()
    mycursor.execute(query)
    data = queryResToString(mycursor) 
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return data

@users.route("/vehicles")
def viewVehiclesRows():
    query = f"SELECT * FROM vehicles"
    [mycursor, mydb] = openConnection()
    mycursor.execute(query)
    data = queryResToString(mycursor) 
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return data

@users.route("/reservations/<user_id>", methods = ['GET', 'POST'])
def createReservations(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    
    if request.method == 'POST':
        fields = ["point_id","effective_timestamp"]

        # Check if request content type is json
        if not request.content_type == 'application/json': 
            return {"status": 400, "msg": "Provide data in JSON format "}
        # Check if JSON body is empty
        if str(request.data) == "b''":
            return {"status": 400, "msg": "Provide body data "}
        # Check for every field needed 
        data = request.json
        for f in fields:
            if f not in data:
                return {"status": 400, "msg": "Invalid request for field " + f}
        
        # Execute query
        [mycursor, mydb] = openConnection()
        mycursor.execute( """INSERT IGNORE INTO reservations (user_id, point_id, effective_timestamp)
                            VALUES (%s,%s,%s)""" , (user_id,data['point_id'], data['effective_timestamp']))  
        mydb.commit()  
        # Return results
        if not mycursor.rowcount:
            return {"status": 402, "msg": "There is already a reservation with the same data, try a different slot or a different timestamp"}
        else:
            return {"status": 200, "msg": "Your reservation was successfully created."}
    if request.method == 'GET':
        [mycursor,mydb] = openConnection()
        query = f"SELECT * FROM reservations where user_id = {user_id}"
        mycursor.execute(query)
        data = queryToDictList(mycursor)
        res = {"status": 200, "msg": data}
        res = dateTimeDictToString(res)
        if not mycursor.rowcount:
            closeConnection(mydb,mycursor)
            return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
        else:
            closeConnection(mydb,mycursor)
        return res
 
@users.route("/charge/<user_id>", methods = ['POST'])
def chargeNow(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    
    fields = ["point_id", "station_id", "transaction_id", "plate_number", "cost_per_kwh", "connection_time", "disconnection_time", "kwh_delivered", "fast_charging"]

    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    # Check for every field needed 
    data = request.json
    session_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(24))
    for f in fields:
        if f not in data:
            if f == 'transaction_id' : data[f] = 'NULL'
            else :
                return {"status": 400, "msg": "Invalid request for field " + f}
    
    # Execute query
    [mycursor, mydb] = openConnection()
    mycursor.execute( """INSERT IGNORE INTO sessions (session_id, user_id, point_id, station_id, transaction_id, plate_number, cost_per_kwh, connection_time, disconnection_time, kwh_delivered, fast_charging)
                        VALUES (%s,%s,%s, %s,%s,%s, %s,%s,%s, %s,%s)""" , (session_id, user_id,  data['point_id'], data['station_id'], data['transaction_id'], data['plate_number'], data['cost_per_kwh'], data['connection_time'], data['disconnection_time'], data['kwh_delivered'], data['fast_charging']))  
    data_ts = computeGraph(data['connection_time'], data['disconnection_time'], data['kwh_delivered'])
    mycursor.execute( """INSERT IGNORE INTO sessions_time_series (session_id, time_series, mean, variation)
                         VALUES (%s,%s,%s, %s)""" , (session_id, data_ts['time_series'],  data_ts['mean'], data_ts['variation']))
    query = f"SELECT * FROM user_vehicles where user_id = {user_id} and plate_number = '{data['plate_number']}'"
    mycursor.execute(query)
    vehi =  queryToDictList(mycursor)
    battery_update = vehi[0]['current_battery'] + data['kwh_delivered']
    batt_per_upd = round(battery_update*vehi[0]['current_battery_percentage'] / vehi[0]['current_battery'], 1)
    mycursor.execute( """UPDATE user_vehicles 
                        SET current_battery_percentage = %s,
                        current_battery = %s
                        WHERE user_id = %s and plate_number = %s""" , (batt_per_upd,battery_update,user_id,data['plate_number'] ))  
    mydb.commit()  
    # Return results
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There is already a session with the same data. Please check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
        return {"status": 200, "msg": "Your charge was successfully completed."}


@users.route("/payment/<user_id>", methods = ['POST'])
def payNow(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    
    fields = ["payment_timestamp", "amount", "payment_method", "price_policy"]
    # Check if request content type is json
    if not request.content_type == 'application/json': 
        return {"status": 400, "msg": "Provide data in JSON format "}
    # Check if JSON body is empty
    if str(request.data) == "b''":
        return {"status": 400, "msg": "Provide body data "}
    # Check for every field needed 
    data = request.json
    for f in fields:
        if f not in data:
            return {"status": 400, "msg": "Invalid request for field " + f}
            
    [mycursor, mydb] = openConnection()
    if data['payment_method'] == 'Wallet' : 
        query = f"SELECT * FROM user_wallets where user_id = {user_id}"
        mycursor.execute(query)
        wallet_amount =  queryToDictList(mycursor)
        wallet_update = wallet_amount[0]['wallet'] - data['amount']
        if wallet_update < 0 : return {"status": 402, "msg": "Not enough money in wallet. Please update your wallet balance and try again. :("}
        mycursor.execute( """UPDATE user_wallets SET wallet = %s
                            WHERE user_id = %s""" , (wallet_update ,user_id))  
        mydb.commit()  
        # Return results
        if not mycursor.rowcount:
            closeConnection(mydb,mycursor)
            return {"status": 402, "msg": "There was an error with your update. Please, check your data and try again"}
    transaction_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(20))
    # Execute query
    mycursor.execute( """INSERT IGNORE INTO transactions (transaction_id, user_id, payment_timestamp, amount, payment_method, price_policy)
                        VALUES (%s,%s,%s,%s,%s,%s)""" , (transaction_id, user_id,  data['payment_timestamp'], data['amount'], data['payment_method'], data['price_policy']))  
    mydb.commit()  
    # Return results
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There is already a transaction with the same data. Please check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
        return {"status": 200, 
                "msg": "Your payment was successfully completed.",
                "transaction_id": transaction_id}
    

@users.route("/sessions/<user_id>")
def getSessions(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity don't match"}
    query = f"SELECT sessions.*, sessions_time_series.* FROM sessions, sessions_time_series where sessions.user_id = {user_id} and sessions_time_series.session_id = sessions.session_id "
    [mycursor, mydb] = openConnection()    
    mycursor.execute(query)
      # Return results
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return queryResToString(mycursor)

@users.route("/lastsession/<user_id>")
def getLastSession(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity don't match"}
    [mycursor, mydb] = openConnection()    
    mycursor.execute("""SELECT sessions.*, sessions_time_series.* 
                        FROM sessions, sessions_time_series 
                        WHERE sessions.user_id = %s and sessions_time_series.session_id = sessions.session_id ORDER BY sessions.connection_time DESC
                        LIMIT 1""",(user_id,))
    desc = mycursor.description
    column_names = [col[0] for col in desc]
    for row in mycursor.fetchall():
        data = dict(zip(column_names, row))
    closeConnection(mydb,mycursor)
    return data

@users.route("/user/<user_id>")
def viewProfile(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity don't match"}
    query = f"SELECT * FROM users where users.id = {user_id} "
    [mycursor, mydb] = openConnection()
    mycursor.execute(query)
    data = json.dumps(queryToDictList(mycursor)[0])
      # Return results
    if not mycursor.rowcount:
        closeConnection(mydb,mycursor)
        return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
    else:
        closeConnection(mydb,mycursor)
    return data

@users.route("/wallet/<user_id>", methods = ['POST', 'GET'])
def readWallet(user_id):
    payload = jwt.decode(request.headers.get('charge_evolution_token'), current_app.config['SECRET_KEY'] , algorithms="HS256")
    if str(payload['id']) != str(user_id): return {"status": 401, "msg": "User id parameter and identity dont match"}
    [mycursor, mydb] = openConnection()
    if request.method == 'GET':
        query = f"SELECT * FROM user_wallets where user_id = {user_id}"
        mycursor.execute(query)
        data = json.dumps(queryToDictList(mycursor)[0])
        # Return results
        if not mycursor.rowcount:
            closeConnection(mydb,mycursor)
            return {"status": 402, "msg": "There was an error with the procedure. Please, check your data and try again"}
        else:
            closeConnection(mydb,mycursor)
        return data
    
    elif request.method == 'POST':
        fields = ["amount"]
        # Check if request content type is json
        if not request.content_type == 'application/json': 
            return {"status": 400, "msg": "Provide data in JSON format "}
        # Check if JSON body is empty
        if str(request.data) == "b''":
            return {"status": 400, "msg": "Provide body data "}
        # Check for every field needed 
        data = request.json
        if 'amount' not in data: return {"status": 400, "msg": "Invalid request for field amount"}
        # Execute query
        query = f"SELECT * FROM user_wallets where user_id = {user_id}"
        mycursor.execute(query)
        wallet_amount =  queryToDictList(mycursor)
        wallet_update = wallet_amount[0]['wallet'] + data['amount']
        mycursor.execute( """UPDATE user_wallets SET wallet = %s
                            WHERE user_id = %s""" , (wallet_update ,user_id))  
        mydb.commit()  
        # Return results
        if not mycursor.rowcount:
            closeConnection(mydb,mycursor)
            return {"status": 402, "msg": "There was an error with your update. Please, check your data and try again"}
        else:
            closeConnection(mydb,mycursor)
            return {"status": 200, "msg": "Your wallet balance was successfully updated."}
    


@users.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Content-Type'] = 'application/json'
    return response




    

        
    



    






