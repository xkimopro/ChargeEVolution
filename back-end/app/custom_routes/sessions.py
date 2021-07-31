from flask import Blueprint, request,current_app
import datetime
import jwt
import re
import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from db import *
from functions.conversions import *

sessions = Blueprint('sessions', __name__)

@sessions.before_request
def auth_middleware():
    
    try: 
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="chargeevolution")
    except Exception as e: 
        return {"status": 500 , "msg" : "Database unavailable"}

    jwt_token = request.headers.get('charge_evolution_token') 
    if not jwt_token: return {"status": 401, "msg": "No token "} 
    
    try:
        #  If token is valid check if user is admin
        payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
        if not payload['admin'] : return {"status": 401, "msg": "Not authorized"} 
        # Then check if token is blacklisted
        mycursor.execute( "SELECT * FROM token_blacklist WHERE token= %s ", (jwt_token, ) ) 
        if mycursor.rowcount == 1:
            return {"status": 401, "msg": "Token expired. Login again"}

    except jwt.ExpiredSignatureError:
        return {"status": 400, "msg": "Expired token "}
    except jwt.InvalidTokenError:
        return {"status": 400, "msg": "Invalid token "}



@sessions.route("/point/<point_id>/<date_from>/<date_to>")
def getSessionsPerPoint(point_id,date_from,date_to):
    mycursor.execute("""SELECT points.point_id, operators.title, sessions.session_id, sessions.connection_time, 
                        sessions.disconnection_time , connectors.level, 
                        sessions.kwh_delivered , transactions.payment_method , vehicles.type
                        FROM sessions , operators , points, transactions, stations, connectors, user_vehicles , vehicles
                        WHERE points.point_id = %s and sessions.point_id = points.point_id and sessions.station_id = stations.station_id and stations.operator_id =  operators.operator_id 
                        and points.connection_uuid = connectors.uuid and transactions.transaction_id = sessions.transaction_id 
                        and sessions.plate_number = user_vehicles.plate_number and user_vehicles.vehicle_id = vehicles.id
                        and DATE(connection_time) >= %s and DATE(disconnection_time) <=  %s    """ ,(point_id,date_from,date_to) )
    
    data = queryToDictList(mycursor)
    res = dict()
    res['point_id'] = point_id
    res['request_timestamp'] = datetime.datetime.now()  
    res['period_from'] = date_from
    res['period_to'] = date_to   
    res['total_sessions'] = len(data)
    if data == []:  
        res['operator']= 'uknown'
        return res
    res['operator'] = data[0]['title']
    lst = []
    for index,d in enumerate(data):
        tmp = dict()
        tmp['session_index'] = index+1
        tmp['session_id'] = d['session_id']
        tmp['started_on'] = d['connection_time']
        tmp['finished_on'] = d['disconnection_time']
        tmp['protocol'] = d['level']
        tmp['energy_delivered'] = float(d['kwh_delivered'])
        tmp['payment_method'] = d['payment_method']
        tmp['vehicle_type'] = d['type']
        lst.append(tmp)
    res['sessions_list'] = lst
    return res
    
        
@sessions.route("/station/<station_id>/<date_from>/<date_to>")
def getSessionsPerStation(station_id, date_from, date_to):
    mycursor.execute("""SELECT sessions.station_id , operators.title, sessions.point_id, sessions.kwh_delivered
                        from sessions , operators, stations
                        where sessions.station_id = %s AND sessions.station_id = stations.station_id AND stations.operator_id = operators.operator_id  
                        AND DATE(connection_time) >= %s AND DATE(disconnection_time) <=  %s    """ ,(station_id,date_from,date_to) )

    point_sess = queryToDictList(mycursor)
    data = dict()
    data['station_id'] = station_id
    data['request_timestamp'] = datetime.datetime.now()  
    data['period_from'] = date_from
    data['period_to'] = date_to
    data['total_energy_delivered'] = 0
    data['number_charging_sessions'] = len(point_sess)
    data['number_active_points'] = 0
    if point_sess == []:  
        data['operator']= 'uknown'
        return data
    data['operator'] = point_sess[0]['title']
    points_set = set()
    point_lst = []
    for s in point_sess:
        data['total_energy_delivered'] += s['kwh_delivered']
        if (s['point_id'] in points_set):
            findAndEditEntry(point_lst,s['point_id'],s['kwh_delivered'])
        else:
            points_set.add(s['point_id'])
            tmp = dict()
            tmp['point_id'] = s['point_id']
            tmp['point_sessions'] = 1
            tmp['energy_delivered'] = s['kwh_delivered']
            point_lst.append(tmp)

    data['sessions_summary_list'] = point_lst

    data['number_active_points'] = len(points_set)
    return data

@sessions.route("/ev/<vehicle_id>/<date_from>/<date_to>")
def getSessionsPerEV(vehicle_id, date_from, date_to):
    mycursor.execute("""SELECT sessions.plate_number, sessions.kwh_delivered, sessions.session_id, providers.title,
                        sessions.connection_time, sessions.disconnection_time, sessions.point_id, 
                        transactions.price_policy, sessions.cost_per_kwh, transactions.amount
                        FROM sessions, transactions, stations, providers
                        WHERE sessions.plate_number = %s AND sessions.transaction_id = transactions.transaction_id 
                        AND sessions.station_id = stations.station_id and stations.provider_id = providers.provider_id 
                        and DATE(sessions.connection_time) >= %s and DATE(sessions.disconnection_time) <= %s """, (vehicle_id, date_from, date_to))
    data = queryToDictList(mycursor)
    res = dict()
    res['vehicle_id'] = vehicle_id
    res['request_timestamp'] = datetime.datetime.now()  
    res['period_from'] = date_from
    res['period_to'] = date_to
    ev_sessions_lst = []
    points_set = set()
    total_energy = 0
    for index,s in enumerate(data):
        points_set.add(s['point_id'])
        tmp = dict()
        tmp['session_index'] = index+1
        tmp['session_id'] = s['session_id']
        tmp['energy_provider'] = s['title']
        tmp['started_on'] = s['connection_time']
        tmp['finished_on'] = s['disconnection_time']
        tmp['energy_delivered'] = float(s['kwh_delivered'])
        total_energy += float(s['kwh_delivered'])
        tmp['price_policy'] = s['price_policy']
        tmp['session_cost'] = s['amount']
        tmp['cost_per_kwh'] = s['cost_per_kwh']
        ev_sessions_lst.append(tmp)
    res['sessions_list'] = ev_sessions_lst
    res['total_energy'] = total_energy
    res['total_points'] = len(points_set)
    res['total_sessions'] = len(data)

    return res


@sessions.route("/provider/<provider_id>/<date_from>/<date_to>")
def getSessionsPerProvider(provider_id, date_from, date_to):
    mycursor.execute("""select providers.provider_id, providers.title, sessions.station_id , sessions.session_id
                        , sessions.plate_number , sessions.connection_time, sessions.disconnection_time, sessions.kwh_delivered, 
                        transactions.price_policy , sessions.cost_per_kwh, transactions.amount
                        from sessions, providers, transactions, stations 
                        where providers.provider_id = %s and providers.provider_id = stations.provider_id and 
                        stations.station_id = sessions.station_id 
                        and transactions.transaction_id = sessions.transaction_id and DATE(sessions.connection_time) >= %s 
                        and DATE(sessions.disconnection_time) <= %s   """, (provider_id,date_from,date_to))
    data = queryToDictList(mycursor)
    res = dict()
    res['provider_id'] = provider_id
    res['provided_name'] = data[0]['title']
    ev_sessions_lst = []
    total_cost = 0
    for s in data:
        tmp = dict()
        tmp['station_id'] = s['station_id']
        tmp['session_id'] = s['session_id']
        tmp['vehicle_id'] = s['plate_number']                        
        tmp['started_on'] = s['connection_time']
        tmp['finished_on'] = s['disconnection_time']
        tmp['energy_delivered'] = float(s['kwh_delivered'])
        tmp['price_policy'] = s['price_policy']
        tmp['cost_per_kwh'] = s['cost_per_kwh']
        total_cost += s['amount']
        ev_sessions_lst.append(tmp)
    res['total_cost'] = round(total_cost,2)
    res['sessions_list'] = ev_sessions_lst
    return res

@sessions.after_request
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

