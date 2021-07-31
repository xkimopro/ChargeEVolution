import json
import io
import csv
from flask import Blueprint, request,current_app,Response

def nestedToCsv(json_nested):
    print("asdasd")
    keys_prefix = []
    values_prefix = []
    keys_postfix = []
    values_postfix = []
    list_found = False
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    for j in json_nested.items():
        if isinstance(j[1], list):
            the_list = j[1]
            keys_list = list(j[1][0].keys())
            list_found = True
            continue

        if list_found:
            keys_postfix.append(j[0])
            values_postfix.append(j[1])
        else:
            keys_prefix.append(j[0])
            values_prefix.append(j[1])
    print(list_found)
    if list_found:
        # keys_prefix + keys_list + keys_postfix + ["\n"]
        total_keys = keys_prefix + keys_list + keys_postfix
        writer.writerow(total_keys)
        for json in the_list:
            tmp = []
            for j in json.items():
                tmp.append(j[1])
            total_values = values_prefix + tmp + values_postfix
            writer.writerow(total_values)
    else:
        writer.writerow(keys_prefix)
        writer.writerow(values_prefix)

    print(output)
    return output.getvalue().replace('"', '')
        
   

def pureJsonListToCsv(json_list):
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(json_list[0].keys())
    for json in json_list:
        csv_lst = []
        for j in json.items():
            csv_lst.append(str(j[1]))
        writer.writerow(csv_lst)
    return output.getvalue().replace('"', '')



def checkIfNested(obj):
    res_csv = "Empty"
    print(res_csv)
    if isinstance(obj, dict):
        res_csv = nestedToCsv(obj)
    else:
        res_csv = pureJsonListToCsv(obj)

    return res_csv



def queryResToString(mycursor):
    desc = mycursor.description
    column_names = [col[0] for col in desc]
    data = json.dumps([dict(zip(column_names, row)) 
            for row in mycursor.fetchall()])
    return data

def queryToDictList(mycursor):
    desc = mycursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) 
            for row in mycursor.fetchall()]
    return data

def queryResToStringDateTimes(mycursor):
    desc = mycursor.description
    column_names = [col[0] for col in desc]
    data = [dict(zip(column_names, row)) 
            for row in mycursor.fetchall()]
    data = json.dumps(data, indent=4, sort_keys=True, default=str) # Datetime is not serializable
    return data

def dateTimeDictToString(data):
    return json.dumps(data, indent=4, sort_keys=True, default=str) # Datetime is not serializable



def findAndEditEntry(point_lst,point_id,energy_delivered):
    for p in point_lst:
        if p['point_id'] == point_id:
            p['point_sessions'] += 1
            p['energy_delivered'] += energy_delivered



def jwtValidationAndDecode(jwt_token):
    try:
        # Validate cookie
        payload = jwt.decode(jwt_token, current_app.config['SECRET_KEY'] , algorithms="HS256")
        # Then check if token is blacklisted
        mycursor.execute( "SELECT * FROM token_blacklist WHERE token= %s ", (jwt_token, ) ) 
        if mycursor.rowcount == 1:
            return {"status": 401, "msg": "Token expired. Login again"}
        return {"status": 200, "msg": payload }
    except jwt.ExpiredSignatureError:
        return {"status": 400, "msg": "Expired token "}
    except jwt.InvalidTokenError:
        return {"status": 400, 'msg': "Invalid token "}

    




    
        



